import argparse
import configparser
import datetime
import json
import os
import re
import time
from collections import namedtuple

import numpy as np
import openai
import tenacity
import tiktoken

from get_paper import Paper

ReviewerParams = namedtuple(
    "Params", ["paper_path", "file_format", "research_fields", "language"]
)


# 定义Reviewer类
class Reviewer:
    # 初始化方法，设置属性
    def __init__(self, args=None):
        if args.language == 'en':
            self.language = 'English'
        elif args.language == 'zh':
            self.language = 'Chinese'
        else:
            self.language = 'Chinese'
            # 创建一个ConfigParser对象
        self.config = configparser.ConfigParser()
        # 读取配置文件
        self.config.read('apikey.ini')
        OPENAI_KEY = os.environ.get("OPENAI_KEY", "")
        # 获取某个键对应的值
        self.chat_api_list = self.config.get('OpenAI', 'OPENAI_API_KEYS')[1:-1].replace('\'', '').split(',')
        self.chat_api_list.append(OPENAI_KEY)

        # prevent short strings from being incorrectly used as API keys.
        self.chat_api_list = [api.strip() for api in self.chat_api_list if len(api) > 20]
        self.cur_api = 0
        self.file_format = args.file_format
        self.max_token_num = 4096
        self.encoding = tiktoken.get_encoding("gpt2")

    def validateTitle(self, title):
        # 修正论文的路径格式
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_title = re.sub(rstr, "_", title)  # 替换为下划线
        return new_title

    def review_by_chatgpt(self, paper_list):
        htmls = []
        for paper_index, paper in enumerate(paper_list):
            sections_of_interest = self.stage_1(paper)
            # extract the essential parts of the paper
            text = ''
            text += 'Title:' + paper.title + '. '
            text += 'Abstract: ' + paper.section_texts['Abstract']
            intro_title = next((item for item in paper.section_names if 'ntroduction' in item.lower()), None)
            if intro_title is not None:
                text += 'Introduction: ' + paper.section_texts[intro_title]
            # Similar for conclusion section
            conclusion_title = next((item for item in paper.section_names if 'onclusion' in item), None)
            if conclusion_title is not None:
                text += 'Conclusion: ' + paper.section_texts[conclusion_title]
            for heading in sections_of_interest:
                if heading in paper.section_names:
                    text += heading + ': ' + paper.section_texts[heading]
            chat_review_text = self.chat_review(text=text)
            htmls.append('## Paper:' + str(paper_index + 1))
            htmls.append('\n\n\n')
            htmls.append(chat_review_text)

            # 将审稿意见保存起来
            date_str = str(datetime.datetime.now())[:13].replace(' ', '-')
            export_path = os.path.join(self.root_path, 'export')
            if not os.path.exists(export_path):
                os.makedirs(export_path)
            mode = 'w' if paper_index == 0 else 'a'
            file_name = os.path.join(export_path,
                                     date_str + '-' + self.validateTitle(paper.title) + "." + self.file_format)
            self.export_to_markdown("\n".join(htmls), file_name=file_name, mode=mode)
            htmls = []

    def stage_1(self, paper):
        htmls = []
        text = ''
        text += 'Title: ' + paper.title + '. '
        text += 'Abstract: ' + paper.section_texts['Abstract']
        openai.api_key = self.chat_api_list[self.cur_api]
        self.cur_api += 1
        self.cur_api = 0 if self.cur_api >= len(self.chat_api_list) - 1 else self.cur_api
        messages = [
            {"role": "system",
             "content": f"You are a professional reviewer in the field of {args.research_fields}. "
                        f"I will give you a paper. You need to review this paper and discuss the novelty and originality of ideas, correctness, clarity, the significance of results, potential impact and quality of the presentation. "
                        f"Due to the length limitations, I am only allowed to provide you the abstract, introduction, conclusion and at most two sections of this paper."
                        f"Now I will give you the title and abstract and the headings of potential sections. "
                        f"You need to reply at most two headings. Then I will further provide you the full information, includes aforementioned sections and at most two sections you called for.\n\n"
                        f"Title: {paper.title}\n\n"
                        f"Abstract: {paper.section_texts['Abstract']}\n\n"
                        f"Potential Sections: {paper.section_names[2:-1]}\n\n"
                        f"Follow the following format to output your choice of sections:"
                        f"{{chosen section 1}}, {{chosen section 2}}\n\n"},
            {"role": "user", "content": text},
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        result = ''
        for choice in response.choices:
            result += choice.message.content
        print(result)
        return result.split(',')

    @tenacity.retry(wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
                    stop=tenacity.stop_after_attempt(5),
                    reraise=True)
    def chat_review(self, text):
        openai.api_key = self.chat_api_list[self.cur_api]
        self.cur_api += 1
        self.cur_api = 0 if self.cur_api >= len(self.chat_api_list) - 1 else self.cur_api
        review_prompt_token = 1000
        text_token = len(self.encoding.encode(text))
        input_text_index = int(len(text) * (self.max_token_num - review_prompt_token) / text_token)
        input_text = "This is the paper for your review:" + text[:input_text_index]
        with open('ReviewFormat.txt', 'r') as file:  # 读取特定的审稿格式
            review_format = file.read()
        messages = [
            {"role": "system",
             "content": "You are a professional reviewer in the field of " + args.research_fields + ". Now I will give you a paper. You need to give a complete review opinion according to the following requirements and format:" + review_format + " Please answer in {}.".format(
                 self.language)},
            {"role": "user", "content": input_text},
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        result = ''
        for choice in response.choices:
            result += choice.message.content
        print("********" * 10)
        print(result)
        print("********" * 10)
        print("prompt_token_used:", response.usage.prompt_tokens)
        print("completion_token_used:", response.usage.completion_tokens)
        print("total_token_used:", response.usage.total_tokens)
        print("response_time:", response.response_ms / 1000.0, 's')
        return result

    def export_to_markdown(self, text, file_name, mode='w'):
        # 使用markdown模块的convert方法，将文本转换为html格式
        # html = markdown.markdown(text)
        # 打开一个文件，以写入模式
        with open(file_name, mode, encoding="utf-8") as f:
            # 将html格式的内容写入文件
            f.write(text)


def chat_reviewer_main(args):
    reviewer1 = Reviewer(args=args)
    # 开始判断是路径还是文件：   
    paper_list = []
    if args.paper_path.endswith(".pdf"):
        paper_list.append(Paper(path=args.paper_path))
    else:
        for root, dirs, files in os.walk(args.paper_path):
            print("root:", root, "dirs:", dirs, 'files:', files)  # 当前目录路径
            for filename in files:
                # 如果找到PDF文件，则将其复制到目标文件夹中
                if filename.endswith(".pdf"):
                    paper_list.append(Paper(path=os.path.join(root, filename)))
    print("------------------paper_num: {}------------------".format(len(paper_list)))
    [print(paper_index, paper_name.path.split('\\')[-1]) for paper_index, paper_name in enumerate(paper_list)]
    reviewer1.review_by_chatgpt(paper_list=paper_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper_path", type=str, default='', help="path of papers")
    parser.add_argument("--file_format", type=str, default='txt', help="output file format")
    parser.add_argument("--research_fields", type=str,
                        default='computer science, artificial intelligence and reinforcement learning',
                        help="the research fields of paper")
    parser.add_argument("--language", type=str, default='en', help="output lauguage, en or zh")

    reviewer_args = ReviewerParams(**vars(parser.parse_args()))
    start_time = time.time()
    chat_reviewer_main(args=reviewer_args)
    print("review time:", time.time() - start_time)
