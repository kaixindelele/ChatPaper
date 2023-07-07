import tiktoken
from random import shuffle

# `tokenizer`: used to count how many tokens
tokenizer_name = tiktoken.encoding_for_model('gpt-4')
tokenizer = tiktoken.get_encoding(tokenizer_name.name)

def tiktoken_len(text):
    # evaluate how many tokens for the given text
    tokens = tokenizer.encode(text, disallowed_special=())
    return len(tokens)


class Knowledge:
    def __init__(self, db):
        self.db = db
        self.contents = []

    def collect_knowledge(self, keywords_dict, max_query):
        """
        keywords_dict:
            {"machine learning": 5, "language model": 2};
        """
        db = self.db
        if max_query > 0:
            for kw in keywords_dict:
                docs = db.similarity_search_with_score(kw, k=max_query)
                for i in range(max_query):
                    content = {"content": docs[i][0].page_content.replace('\n', ' '),
                               "score": docs[i][1]}  # todo: add more meta information; clean the page_content
                    self.contents.append(content)
            # sort contents by score / shuffle
            shuffle(self.contents)

    def to_prompts(self, max_tokens=2048):
        if len(self.contents) == 0:
            return ""
        prompts = []
        tokens = 0
        for idx, content in enumerate(self.contents):
            prompt = "Reference {}: {}\n".format(idx, content["content"])
            tokens += tiktoken_len(prompt)
            if tokens >= max_tokens:
                break
            else:
                prompts.append(prompt)
        return "".join(prompts)

    def to_json(self):
        if len(self.contents) == 0:
            return {}
        output = {}
        for idx, content in enumerate(self.contents):
            output[str(idx)] = {
                "content": content["content"],
                "score": str(content["score"])
            }
        print(output)
        return output


