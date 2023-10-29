import scipdf
import sys, os
import openai
import tenacity
import tiktoken
import re
from functools import lru_cache


class LazyloadTiktoken(object):
    def __init__(self, model):
        self.model = model

    @staticmethod
    @lru_cache(maxsize=128)
    def get_encoder(model):
        print('正在加载tokenizer，如果是第一次运行，可能需要一点时间下载参数')
        tmp = tiktoken.encoding_for_model(model)
        print('加载tokenizer完毕')
        return tmp
    
    def encode(self, *args, **kwargs):
        encoder = self.get_encoder(self.model) 
        return encoder.encode(*args, **kwargs)
    
    def decode(self, *args, **kwargs):
        encoder = self.get_encoder(self.model) 


def parse_pdf(path):        
    try:
        pdf = scipdf.parse_pdf_to_dict(path, as_list=False)
        # 下面这段内容，可以加，也可以删除        
        pdf['authors'] = pdf['authors'].split('; ')
        pdf['section_names'] = [it['heading'] for it in pdf['sections']]
        pdf['section_texts'] = [it['text'] for it in pdf['sections']]
    except Exception as e:
        print("parse_pdf_to_dict(path:", e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)     
    return pdf

@tenacity.retry(wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
                    stop=tenacity.stop_after_attempt(8),
                    reraise=True)
def chat_translate_part(text, key, title=False, domain="", tokenizer_gpt35=None, task="翻译"):
    openai.api_key = key
    # 这里需要做切分，如果长文本的话，需要多次翻译，或者直接换用16K的api.
    # 先判断文本token长度：
    token_size = len(tokenizer_gpt35.encode(text))
    if token_size > 1800:
        model = "gpt-3.5-turbo-16k"
    else:
        model = "gpt-3.5-turbo"    
    
    if title:
        messages = [
            {"role": "system",
                "content": "You are now a professional Science and technology editor"},
            {"role": "assistant",
                "content": "Your task now is to translate title of the paper, the paper is about "+ domain},
            {"role": "user", "content": "Input Contents:" + text +                
                
                """
                你需要把输入的标题，翻译成中文，且加上原标题。
                注意，一些专业的词汇，或者缩写，还是需要保留为英文。
                输出中文翻译部分的时候，只保留翻译的标题，不要有任何其他的多余内容，不要重复，不要解释。
                输出原标题的时候，完整输出即可，不要多也不要少。
                你的输出格式如下：
                Output format is (你需要根据上面的要求，xxx是中文翻译的占位符，yyy是英文原标题的占位符，你需要将内容填充进去):
                \n        
                # xxx
                
                ## yyy
                \n    
                """},
        ]
    else:
        messages = [
            {"role": "system",
                "content": "You are a professional academic paper translator."},
            {"role": "assistant",
                "content": "Your task now is to {} the Input Contents, which a section, part of a paper, the paper is about {}".format(task, domain)},
            {"role": "user", "content": f"""
                你的任务是口语化{task}输入的论文章节，{task}的内容要遵循下面的要求：
                1. 在保证术语严谨的同时，文字表述需要更加口语化。
                2. 需要地道的中文{task}，逻辑清晰且连贯，少用倒装句式。
                3. 对于简短的Input Contents，不要画蛇添足，增加多余的解释和扩展。
                4. 对于本领域的专业术语，需要标注英文，便于读者参考。这篇论文的领域是{domain}。
                5. 适当使用MarkDown语法，比如有序列表、加粗等。
                
                你的输出内容格式需要遵循下面的要求：
                1. ## 章节名称，中文{task}(Original English section name)
                2. 章节内容的{task}

                Output format is (你需要根据上面的要求，自动填充xxx和yyy的占位符):
                \n        
                ## xxx
                
                yyy
                \n
                
                Input include section name and section text, Input Contents: {text}                          
                """},
        ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.3,
    )
    result = ''
    for choice in response.choices:
        result += choice.message.content
    print("summary_result:\n", result)
    print("prompt_token_used:", response.usage.prompt_tokens,
            "completion_token_used:", response.usage.completion_tokens,
            "total_token_used:", response.usage.total_tokens)
    print("response_time:", response.response_ms / 1000.0, 's')
    info = {}
    info['result'] = result
    info['token_used'] = response.usage.total_tokens
    info['response_time'] = response.response_ms / 1000.0
    return info

@tenacity.retry(wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
                    stop=tenacity.stop_after_attempt(8),
                    reraise=True)
def chat_check_domain(text, key):
    openai.api_key = key
    messages = [
            {"role": "system",
                "content": "You are now a professional Science and technology editor"},
            {"role": "assistant",
                "content": "Your task is to judge the subject and domain of the paper based on the title and abstract of the paper, and your output should not exceed five words!"},
            {"role": "user", "content": "Input Contents:" + text},
        ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.3,
    )
    result = ''
    for choice in response.choices:
        result += choice.message.content
    print("summary_result:\n", result)
    print("prompt_token_used:", response.usage.prompt_tokens,
            "completion_token_used:", response.usage.completion_tokens,
            "total_token_used:", response.usage.total_tokens)
    print("response_time:", response.response_ms / 1000.0, 's')
    info = {}
    info['result'] = result
    info['token_used'] = response.usage.total_tokens
    info['response_time'] = response.response_ms / 1000.0
    return info

def main(root_path, pdf_path, base_url, key, task="翻译"):
    md_file = root_path + pdf_path.split("/")[-1].replace(".pdf", '.md')
    md_str = "\n"        
    token_consumed = 0
    paper_pdf = parse_pdf(pdf_path)

    
    tokenizer_gpt35 = LazyloadTiktoken("gpt-3.5-turbo")
    
    # 先根据标题和摘要，确定这篇文章的主题，给接下来的提示词，提供一个约束。效果提升非常明显
    if "title" in paper_pdf.keys() and "abstract" in paper_pdf.keys():
        text = "Title:" + paper_pdf['title'] + "Abstract:" + paper_pdf['abstract']
        return_dict = chat_check_domain(text, key)
        domains = return_dict['result']
        token_consumed += return_dict["token_used"]
    else:
        domains = ""
        
    print("这篇文章的domain是：", domains)
    
    # input("继续？")
    openai.api_base = base_url   
    # 先把标题翻译了
    if "title" in paper_pdf.keys():
        text = paper_pdf['title']
        return_dict = chat_translate_part(text, key, title=True, domain=domains, tokenizer_gpt35=tokenizer_gpt35)
        result = return_dict['result']
        md_str += result
        md_str += "\n"
        md_str += "\n"
        token_consumed += return_dict["token_used"]
    with open(md_file, 'w', encoding="utf-8") as f:
        f.write(md_str)
    
    # 再把摘要翻译了
    if "abstract" in paper_pdf.keys():
        text = "Section Name:" + "Abstract" + "\n Section text:" + paper_pdf['abstract']
        return_dict = chat_translate_part(text, key, domain=domains, tokenizer_gpt35=tokenizer_gpt35)
        result = return_dict['result']
        cur_str = "\n"
        cur_str += result
        cur_str += "\n"       
        token_consumed += return_dict["token_used"] 
        with open(md_file, 'a', encoding="utf-8") as f:
            f.write(cur_str)
            
    for section_index, section_name in enumerate(paper_pdf['section_names']):
        print(section_index, section_name)
        # 判断文本是否为空：
        if len(paper_pdf['section_texts'][section_index])>0:
            text = "Section Name:" + section_name + "\n Section text:" + paper_pdf['section_texts'][section_index]
            return_dict = chat_translate_part(text, key, domain=domains, tokenizer_gpt35=tokenizer_gpt35, task=task)
            result = return_dict['result']
            cur_str = "\n"
            cur_str += result
            cur_str += "\n"
            token_consumed += return_dict["token_used"] 
            
            # 找到其中包含##的文本，如果##的前面没有\n，且后面文本到\n的文本长度小于18个word，则将其替换为\n##，否则不替换
            pattern = r'([^\\n])##([^\\n]{1,18}\W+)'
            cur_str = re.sub(pattern, r'\1\n##\2', cur_str) 

            with open(md_file, 'a', encoding="utf-8") as f:
                f.write(cur_str)
                
    print("整篇文章消耗了{}的token！".format(token_consumed))
        


if __name__ == "__main__":
    root_path = r'./'
    pdf_path = r'./demo.pdf'
    base_url = 'https://api.openai.com/v1'
    key = "sk-xxx"
    task = "翻译"
    main(root_path, pdf_path, base_url, key, task)
