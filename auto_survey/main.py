import json
import os.path
import logging
import time
from langchain.vectorstores import FAISS
from langchain import PromptTemplate
from utils.references import References
from utils.knowledge import Knowledge
from utils.file_operations import  make_archive, copy_templates
from utils.tex_processing import create_copies
from utils.gpt_interaction import GPTModel
from utils.prompts import SYSTEM
from utils.embeddings import EMBEDDINGS
from utils.gpt_interaction import get_gpt_responses
TOTAL_TOKENS = 0
TOTAL_PROMPTS_TOKENS = 0
TOTAL_COMPLETION_TOKENS = 0
def log_usage(usage, generating_target, print_out=True):
    global TOTAL_TOKENS
    global TOTAL_PROMPTS_TOKENS
    global TOTAL_COMPLETION_TOKENS

    prompts_tokens = usage['prompt_tokens']
    completion_tokens = usage['completion_tokens']
    total_tokens = usage['total_tokens']

    TOTAL_TOKENS += total_tokens
    TOTAL_PROMPTS_TOKENS += prompts_tokens
    TOTAL_COMPLETION_TOKENS += completion_tokens

    message = f">>USAGE>> For generating {generating_target}, {total_tokens} tokens have been used " \
              f"({prompts_tokens} for prompts; {completion_tokens} for completion). " \
              f"{TOTAL_TOKENS} tokens have been used in total."
    if print_out:
        print(message)
    logging.info(message)


def _generation_setup(title,  template="Default",
                      tldr=False, max_kw_refs=20, bib_refs=None, max_tokens_ref=2048,  # generating references
                      knowledge_database=None, max_tokens_kd=2048, query_counts=10):

    llm = GPTModel(model="gpt-3.5-turbo-16k")
    bibtex_path, destination_folder = copy_templates(template, title)
    logging.basicConfig(level=logging.INFO, filename=os.path.join(destination_folder, "generation.log"))

    #generate key words
    keywords, usage = llm(systems=SYSTEM["keywords"], prompts=title, return_json=True)
    log_usage(usage, "keywords")
    keywords = {keyword: max_kw_refs for keyword in keywords}
    print("Keywords: \n", keywords)

    #generate references
    ref = References(title, bib_refs)
    ref.collect_papers(keywords, tldr=tldr)
    references = ref.to_prompts(max_tokens=max_tokens_ref)
    all_paper_ids = ref.to_bibtex(bibtex_path)

    #product domain knowledge
    prompts = f"Title: {title}"
    preliminaries_kw, _ = llm(systems=SYSTEM["preliminaries"], prompts=prompts)
    # check if the database exists or not
    db_path = f"utils/knowledge_databases/{knowledge_database}"
    db_config_path = os.path.join(db_path, "db_meta.json")
    db_index_path = os.path.join(db_path, "faiss_index")
    if os.path.isdir(db_path):
        try:
            with open(db_config_path, "r", encoding="utf-8") as f:
                db_config = json.load(f)
            model_name = db_config["embedding_model"]
            embeddings = EMBEDDINGS[model_name]
            db = FAISS.load_local(db_index_path, embeddings)
            knowledge = Knowledge(db=db)
            knowledge.collect_knowledge(preliminaries_kw, max_query=query_counts)
            domain_knowledge = knowledge.to_prompts(max_tokens_kd)
        except Exception as e:
            domain_knowledge=''
    prompts = f"Title: {title}"
    syetem_promot =  "You are an assistant designed to propose necessary components of an survey papers. Your response should follow the JSON format."
    components, usage = llm(systems=syetem_promot, prompts=prompts, return_json=True)
    log_usage(usage, "media")
    print(f"The paper information has been initialized. References are saved to {bibtex_path}.")

    paper = {}
    paper["title"] = title
    paper["references"] = references
    paper["bibtex"] = bibtex_path
    paper["components"] = components
    paper["domain_knowledge"] = domain_knowledge
    return paper, destination_folder, all_paper_ids


def section_generation(paper, section, save_to_path, model, research_field="machine learning"):
    """
    The main pipeline of generating a section.
        1. Generate prompts.
        2. Get responses from AI assistant.
        3. Extract the section text.
        4. Save the text to .tex file.
    :return usage
    """

    title = paper["title"]
    references = paper["references"]
    components = paper['components']
    instruction = '- Discuss three to five main related fields to this paper. For each field, select five to ten key publications from references. For each reference, analyze its strengths and weaknesses in one or two sentences. Present the related works in a logical manner, often chronologically. Consider using a taxonomy or categorization to structure the discussion. Do not use \section{...} or \subsection{...}; use \paragraph{...} to list related fields.'


    fundamental_subprompt = "Your task is to write the {section} section of the paper with the title '{title}'. This paper has the following content: {components}\n"
    instruction_subprompt = "\n" \
                            "Your response should follow the following instructions:\n" \
                            "{instruction}\n"


    ref_instruction_subprompt = "- Read references. " \
                                "Every time you use information from the references, you need to appropriately cite it (using \citep or \citet)." \
                                "For example of \citep, the sentence where you use information from lei2022adaptive \citep{{lei2022adaptive}}. " \
                                "For example of \citet, \citet{{lei2022adaptive}} claims some information.\n" \
                                "- Avoid citing the same reference in a same paragraph.\n" \
                                "\n" \
                                "References:\n" \
                                "{references}"
    output_subprompt = "Ensure that it can be directly compiled by LeTaX."

    reivew_prompts = PromptTemplate(
        input_variables=["title", "components", "instruction", "section", "references"],
        template=fundamental_subprompt + instruction_subprompt + ref_instruction_subprompt + output_subprompt)
    prompts = reivew_prompts.format(title=title,
                                    components=components,
                                    instruction=instruction,
                                    section=section,
                                    references=references)
    SECTION_GENERATION_SYSTEM = PromptTemplate(input_variables=["research_field"],
                                               template="You are an assistant designed to write academic papers in the field of {research_field} using LaTeX." )
    output, usage = get_gpt_responses(SECTION_GENERATION_SYSTEM.format(research_field=research_field), prompts,
                                      model=model, temperature=0.4)

    output=output[25:]
    tex_file = os.path.join(save_to_path, f"{section}.tex")
    with open(tex_file, "w", encoding="utf-8") as f:
        f.write(output)

    use_md =True
    use_chinese = True
    if use_md:
        system_md = 'You are an translator between the  LaTeX and .MD. here is a latex file where the content is: \n \n ' + output
        prompts_md = 'you should transfer the latex content to the .MD format seriously, and pay attention to the correctness of the citation format (use the number). you should directly output the new content without anyoter replay. you should add reference papers at the end of the paper, and add line breaks between two reference papers. The Title should be ' + paper['title']
        output_md, usage_md = get_gpt_responses(system_md, prompts_md,
                                          model=model, temperature=0.4)
        md_file = os.path.join(save_to_path, f"{'survey'}.md")
        with open(md_file, "w", encoding="utf-8") as m:
            m.write(output_md)

        if use_chinese == True:
            system_md_chi = 'You are an translator between the  english and chinese. here is a english file where the content is: \n \n ' + output
            prompts_md_chi = 'you should transfer the english to chinese and dont change anything others. you should directly output the new content without anyoter replay. you should keep the reference papers unchanged.'

            output_md_chi, usage_md_chi = get_gpt_responses(system_md_chi, prompts_md_chi,
                                                    model=model, temperature=0.4)
            md_file_chi = os.path.join(save_to_path, f"{'survey_chinese'}.md")
            with open(md_file_chi, "w", encoding="utf-8") as c:
                c.write(output_md_chi)
    return usage


def generate_draft(title,  tldr=True, max_kw_refs=20, bib_refs=None, max_tokens_ref=2048,
                   knowledge_database=None, max_tokens_kd=2048, query_counts=10,
                   section='related works', model="gpt-3.5-turbo-16k", template="Default"
                   , save_zip=None):

    print("================START================")
    paper, destination_folder, _ = _generation_setup(title,  template, tldr, max_kw_refs, bib_refs,
                                                     max_tokens_ref=max_tokens_ref, max_tokens_kd=max_tokens_kd,
                                                     query_counts=query_counts,
                                                     knowledge_database=knowledge_database)

    # main components
    print(f"================PROCESSING================")
    usage = section_generation(paper, section, destination_folder, model=model)
    log_usage(usage, section)
    create_copies(destination_folder)
    print("\nPROCESSING COMPLETE\n")
    return make_archive(destination_folder, title+".zip")
    print("draft has been generated in " + destination_folder)




if __name__ == "__main__":
    import openai

    openai.api_key = "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"
    openai.api_base = 'https://api.openai.com/v1'
    openai.proxy = "socks5h://localhost:7890"
    target_title = "Reinforcement Learning for Robot Control"

    generate_draft(target_title, knowledge_database="ml_textbook_test",max_kw_refs=20)

