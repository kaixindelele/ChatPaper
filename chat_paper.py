import numpy as np
import os
import re
import datetime
import markdown
import arxiv
import openai, tenacity
import base64, requests
import argparse
import configparser
from get_paper_from_pdf import Paper

# 定义Reader类
class Reader:
    # 初始化方法，设置属性
    def __init__(self, key_word, query, filter_keys, 
                 root_path='./',
                 gitee_key='',
                 sort=arxiv.SortCriterion.SubmittedDate, user_name='defualt', language='cn', args=None):
        self.user_name = user_name # 读者姓名
        self.key_word = key_word # 读者感兴趣的关键词
        self.query = query # 读者输入的搜索查询
        self.sort = sort # 读者选择的排序方式
        self.language = language # 读者选择的语言        
        self.filter_keys = filter_keys # 用于在摘要中筛选的关键词
        self.root_path = root_path
        # 创建一个ConfigParser对象
        self.config = configparser.ConfigParser()
        # 读取配置文件
        self.config.read('apikey.ini')
        # 获取某个键对应的值        
        self.chat_api_list = self.config.get('OpenAI', 'OPENAI_API_KEYS')[1:-1].replace('\'', '').split(',')
        self.chat_api_list = [api.strip() for api in self.chat_api_list if len(api) > 5]
        self.cur_api = 0
        self.file_format = args.file_format
        if args.save_image:
            self.gitee_key = self.config.get('Gitee', 'api')
        else:
            self.gitee_key = ''
                
    def get_arxiv(self, max_results=30):
        search = arxiv.Search(query=self.query,
                              max_results=max_results,                              
                              sort_by=self.sort,
                              sort_order=arxiv.SortOrder.Descending,
                              )       
        return search
     
    def filter_arxiv(self, max_results=30):
        search = self.get_arxiv(max_results=max_results)
        print("all search:")
        for index, result in enumerate(search.results()):
            print(index, result.title, result.updated)
            
        filter_results = []   
        filter_keys = self.filter_keys
        
        print("filter_keys:", self.filter_keys)
        # 确保每个关键词都能在摘要中找到，才算是目标论文
        for index, result in enumerate(search.results()):
            abs_text = result.summary.replace('-\n', '-').replace('\n', ' ')
            meet_num = 0
            for f_key in filter_keys:
                if f_key.lower() in abs_text.lower():
                    meet_num += 1
            if meet_num == len(filter_keys):
                filter_results.append(result)
                # break
        print("filter_results:", len(filter_results))
        print("filter_papers:")
        for index, result in enumerate(filter_results):
            print(index, result.title, result.updated)
        return filter_results
    
    def validateTitle(self, title):
        # 将论文的乱七八糟的路径格式修正
        rstr = r"[\/\\\:\*\?\"\<\>\|]" # '/ \ : * ? " < > |'
        new_title = re.sub(rstr, "_", title) # 替换为下划线
        return new_title

    def download_pdf(self, filter_results):
        # 先创建文件夹
        date_str = str(datetime.datetime.now())[:13].replace(' ', '-')        
        key_word = str(self.key_word.replace(':', ' '))        
        path = self.root_path  + 'pdf_files/' + self.query.replace('au: ', '').replace('title: ', '').replace('ti: ', '').replace(':', ' ')[:25] + '-' + date_str
        try:
            os.makedirs(path)
        except:
            pass
        print("All_paper:", len(filter_results))
        # 开始下载：
        paper_list = []
        for r_index, result in enumerate(filter_results):
            try:
                title_str = self.validateTitle(result.title)
                pdf_name = title_str+'.pdf'
                # result.download_pdf(path, filename=pdf_name)
                self.try_download_pdf(result, path, pdf_name)
                paper_path = os.path.join(path, pdf_name)
                print("paper_path:", paper_path)
                paper = Paper(path=paper_path,
                              url=result.entry_id,
                              title=result.title,
                              abs=result.summary.replace('-\n', '-').replace('\n', ' '),
                              authers=[str(aut) for aut in result.authors],
                              )
                # 下载完毕，开始解析：
                paper.parse_pdf()
                paper_list.append(paper)
            except Exception as e:
                print("download_error:", e)
                pass
        return paper_list
    
    @tenacity.retry(wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
                    stop=tenacity.stop_after_attempt(5),
                    reraise=True)
    def try_download_pdf(self, result, path, pdf_name):
        result.download_pdf(path, filename=pdf_name)
    
    @tenacity.retry(wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
                    stop=tenacity.stop_after_attempt(5),
                    reraise=True)
    def upload_gitee(self, image_path, image_name='', ext='png'):
        """
        上传到码云
        :return:
        """ 
        with open(image_path, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            base64_content = base64_data.decode()
        
        date_str = str(datetime.datetime.now())[:19].replace(':', '-').replace(' ', '-') + '.' + ext
        path = image_name+ '-' +date_str
        
        payload = {
            "access_token": self.gitee_key,
            "owner": self.config.get('Gitee', 'owner'),
            "repo": self.config.get('Gitee', 'repo'),
            "path": self.config.get('Gitee', 'path'),
            "content": base64_content,
            "message": "upload image"
        }
        # 这里需要修改成你的gitee的账户和仓库名，以及文件夹的名字：
        url = f'https://gitee.com/api/v5/repos/'+self.config.get('Gitee', 'owner')+'/'+self.config.get('Gitee', 'repo')+'/contents/'+self.config.get('Gitee', 'path')+'/'+path
        rep = requests.post(url, json=payload).json()
        print("rep:", rep)
        if 'content' in rep.keys():
            image_url = rep['content']['download_url']
        else:
            image_url = r"https://gitee.com/api/v5/repos/"+self.config.get('Gitee', 'owner')+'/'+self.config.get('Gitee', 'repo')+'/contents/'+self.config.get('Gitee', 'path')+'/' + path
            
        return image_url
    
    def summary_with_chat(self, paper_list):
        htmls = []
        for paper_index, paper in enumerate(paper_list):
            # 第一步先用title，abs，和introduction进行总结。
            text = ''
            text += 'Title:' + paper.title
            text += 'Url:' + paper.url
            text += 'Abstrat:' + paper.abs
            # intro
            text += list(paper.section_text_dict.values())[0]
            max_token = 2500 * 4
            text = text[:max_token]
            chat_summary_text = self.chat_summary(text=text)            
            htmls.append('## Paper:' + str(paper_index+1))
            htmls.append('\n\n\n')            
            htmls.append(chat_summary_text)
            
            # TODO 往md文档中插入论文里的像素最大的一张图片，这个方案可以弄的更加智能一些：
            first_image, ext = paper.get_image_path()
            if first_image is None or self.gitee_key == '':
                pass
            else:                
                image_title = self.validateTitle(paper.title)
                image_url = self.upload_gitee(image_path=first_image, image_name=image_title, ext=ext)
                htmls.append("\n\n")
                htmls.append("![Fig]("+image_url+")")
                htmls.append("\n\n")
            # 第二步总结方法：
            # TODO，由于有些文章的方法章节名是算法名，所以简单的通过关键词来筛选，很难获取，后面需要用其他的方案去优化。
            method_key = ''
            for parse_key in paper.section_text_dict.keys():
                if 'method' in parse_key.lower() or 'approach' in parse_key.lower():
                    method_key = parse_key
                    break
                
            if method_key != '':
                text = ''
                method_text = ''
                summary_text = ''
                summary_text += "<summary>" + chat_summary_text
                # methods                
                method_text += paper.section_text_dict[method_key]   
                # TODO 把这个变成tenacity的自动判别！             
                max_token = 2500 * 4
                text = summary_text + "\n\n<Methods>:\n\n" + method_text 
                text = text[:max_token]
                chat_method_text = self.chat_method(text=text)
                htmls.append(chat_method_text)
            else:
                chat_method_text = ''
            htmls.append("\n"*4)
            
            # 第三步总结全文，并打分：
            conclusion_key = ''
            for parse_key in paper.section_text_dict.keys():
                if 'conclu' in parse_key.lower():
                    conclusion_key = parse_key
                    break
            
            text = ''
            conclusion_text = ''
            summary_text = ''
            summary_text += "<summary>" + chat_summary_text + "\n <Method summary>:\n" + chat_method_text            
            if conclusion_key != '':
                # conclusion                
                conclusion_text += paper.section_text_dict[conclusion_key]                
                max_token = 2500 * 4
                text = summary_text + "\n\n<Conclusion>:\n\n" + conclusion_text 
            else:
                text = summary_text
            text = text[:max_token]
            chat_conclusion_text = self.chat_conclusion(text=text)
            htmls.append(chat_conclusion_text)
            htmls.append("\n"*4)
            
            # # 整合成一个文件，打包保存下来。
            date_str = str(datetime.datetime.now())[:13].replace(' ', '-')
            try:
                export_path = os.path.join(self.root_path, 'export')
                os.makedirs(export_path)
            except:
                pass                             
            mode = 'w' if paper_index == 0 else 'a'
            file_name = os.path.join(export_path, date_str+'-'+self.validateTitle(paper.title)+"."+self.file_format)
            self.export_to_markdown("\n".join(htmls), file_name=file_name, mode=mode)
            
            # file_name = os.path.join(export_path, date_str+'-'+self.validateTitle(paper.title)+".md")
            # self.export_to_markdown("\n".join(htmls), file_name=file_name, mode=mode)
            htmls = []
            
    @tenacity.retry(wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
                    stop=tenacity.stop_after_attempt(5),
                    reraise=True)
    def chat_conclusion(self, text):
        openai.api_key = self.chat_api_list[self.cur_api]
        self.cur_api += 1
        self.cur_api = 0 if self.cur_api == len(self.chat_api_list)-1 else self.cur_api
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            # prompt需要用英语替换，少占用token。
            messages=[
                {"role": "system", "content": "你是一个["+self.key_word+"]领域的审稿人，你需要严格评审这篇文章"},  # chatgpt 角色
                {"role": "assistant", "content": "这是一篇英文文献的<summary>和<conclusion>部分内容，其中<summary>你已经总结好了，但是<conclusion>部分，我需要你帮忙归纳下面问题："+text},  # 背景知识，可以参考OpenReview的审稿流程
                {"role": "user", "content": """                 
                 8. 做出如下总结：
                    - (1):这篇工作的意义如何？
                    - (2):从创新点、性能、工作量这三个维度，总结这篇文章的优点和缺点。                   
                    .......
                 按照后面的格式输出: 
                 8. Conclusion: \n\n
                    - (1):xxx;\n                     
                    - (2):创新点: xxx; 性能: xxx; 工作量: xxx;\n                      
                 
                 务必使用中文回答（专有名词需要用英文标注)，语句尽量简洁且学术，不要和之前的<summary>内容重复，数值使用原文数字, 务必严格按照格式，将对应内容输出到xxx中，按照\n换行，.......代表按照实际需求填写，如果没有可以不用写.                 
                 """},
            ]
        )
        result = ''
        for choice in response.choices:
            result += choice.message.content
        print("conclusion_result:\n", result)
        return result            
    
    @tenacity.retry(wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
                    stop=tenacity.stop_after_attempt(5),
                    reraise=True)
    def chat_method(self, text):
        openai.api_key = self.chat_api_list[self.cur_api]
        self.cur_api += 1
        self.cur_api = 0 if self.cur_api == len(self.chat_api_list)-1 else self.cur_api
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个["+self.key_word+"]领域的科研人员，善于使用精炼的语句总结论文"},  # chatgpt 角色
                {"role": "assistant", "content": "这是一篇英文文献的<summary>和<Method>部分内容，其中<summary>你已经总结好了，但是<Methods>部分，我需要你帮忙阅读并归纳下面问题："+text},  # 背景知识
                {"role": "user", "content": """                 
                 7. 详细描述这篇文章的方法思路。比如说它的步骤是：
                    - (1):...
                    - (2):...
                    - (3):...
                    - .......
                 按照后面的格式输出: 
                 7. Methods: \n\n
                    - (1):xxx;\n 
                    - (2):xxx;\n 
                    - (3):xxx;\n  
                    .......\n\n     
                 
                 务必使用中文回答（专有名词需要用英文标注)，语句尽量简洁且学术，不要和之前的<summary>内容重复，数值使用原文数字, 务必严格按照格式，将对应内容输出到xxx中，按照\n换行，.......代表按照实际需求填写，如果没有可以不用写.                 
                 """},
            ]
        )
        result = ''
        for choice in response.choices:
            result += choice.message.content
        print("method_result:\n", result)
        return result
    
    @tenacity.retry(wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
                    stop=tenacity.stop_after_attempt(5),
                    reraise=True)
    def chat_summary(self, text):
        openai.api_key = self.chat_api_list[self.cur_api]
        self.cur_api += 1
        self.cur_api = 0 if self.cur_api == len(self.chat_api_list)-1 else self.cur_api
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个["+self.key_word+"]领域的科研人员，善于使用精炼的语句总结论文"},  # chatgpt 角色
                {"role": "assistant", "content": "这是一篇英文文献的标题，作者，链接，Abstract和Introduction部分内容，我需要你帮忙阅读并归纳下面问题："+text},  # 背景知识
                {"role": "user", "content": """                 
                 1. 标记出这篇文献的标题(加上中文翻译)
                 2. 列举所有的作者姓名 (使用英文)
                 3. 标记第一作者的单位（只输出中文翻译）                 
                 4. 标记出这篇文章的关键词(使用英文)
                 5. 论文链接，Github代码链接（如果有的话，没有的话请填写Github:None）
                 6. 按照下面四个点进行总结：
                    - (1):这篇文章的研究背景是什么？
                    - (2):过去的方法有哪些？它们存在什么问题？本文和过去的研究有哪些本质的区别？Is the approach well motivated?
                    - (3):本文提出的研究方法是什么？
                    - (4):本文方法在什么任务上，取得了什么性能？性能能否支持他们的目标？
                 按照后面的格式输出:                  
                 1. Title: xxx\n\n
                 2. Authors: xxx\n\n
                 3. Affiliation: xxx\n\n                 
                 4. Keywords: xxx\n\n   
                 5. Urls: xxx or xxx , xxx \n\n      
                 6. Summary: \n\n
                    - (1):xxx;\n 
                    - (2):xxx;\n 
                    - (3):xxx;\n  
                    - (4):xxx.\n\n     
                 
                 务必使用中文回答（专有名词需要用英文标注)，语句尽量简洁且学术，不要有太多重复的信息，数值使用原文数字, 务必严格按照格式，将对应内容输出到xxx中，按照\n换行.                 
                 """},
            ]
        )
        result = ''
        for choice in response.choices:
            result += choice.message.content
        print("summary_result:\n", result)
        return result        
            
    def export_to_markdown(self, text, file_name, mode='w'):
        # 使用markdown模块的convert方法，将文本转换为html格式
        # html = markdown.markdown(text)
        # 打开一个文件，以写入模式
        with open(file_name, mode, encoding="utf-8") as f:
            # 将html格式的内容写入文件
            f.write(text)        

    # 定义一个方法，打印出读者信息
    def show_info(self):        
        print(f"Key word: {self.key_word}")
        print(f"Query: {self.query}")
        print(f"Sort: {self.sort}")                

def main(args):       
    # 创建一个Reader对象，并调用show_info方法
    if args.pdf_path:
        reader1 = Reader(key_word=args.key_word, 
                         query=args.query, 
                         filter_keys=args.filter_keys,                                    
                         sort=args.sort, 
                         args=args
                         )
        reader1.show_info()
        paper_list = [Paper(path=args.pdf_path)]
        reader1.summary_with_chat(paper_list=paper_list)
    else:
        reader1 = Reader(key_word=args.key_word, 
                         query=args.query, 
                         filter_keys=args.filter_keys,                                    
                         sort=args.sort, 
                         args=args
                         )
        reader1.show_info()
        filter_results = reader1.filter_arxiv(max_results=args.max_results)
        paper_list = reader1.download_pdf(filter_results)
        reader1.summary_with_chat(paper_list=paper_list)
    
    
if __name__ == '__main__':    
    parser = argparse.ArgumentParser()
    # parser.add_argument("--pdf_path", type=str, default=r'demo.pdf', help="if none, the bot will download from arxiv with query")
    parser.add_argument("--pdf_path", type=str, default='', help="if none, the bot will download from arxiv with query")
    parser.add_argument("--query", type=str, default='all: ChatGPT robot', help="the query string, ti: xx, au: xx, all: xx,")    
    parser.add_argument("--key_word", type=str, default='reinforcement learning', help="the key word of user research fields")
    parser.add_argument("--filter_keys", type=str, default='ChatGPT robot', help="the filter key words, 摘要中每个单词都得有，才会被筛选为目标论文")
    parser.add_argument("--max_results", type=int, default=1, help="the maximum number of results")
    parser.add_argument("--sort", default=arxiv.SortCriterion.Relevance, help="another is arxiv.SortCriterion.LastUpdatedDate")    
    parser.add_argument("--save_image", default=False, help="save image? It takes a minute or two to save a picture! But pretty")
    parser.add_argument("--file_format", type=str, default='md', help="导出的文件格式，如果存图片的话，最好是md，如果不是的话，txt的不会乱")
    
    args = parser.parse_args()
    import time
    start_time = time.time()
    main(args=args)    
    print("summary time:", time.time() - start_time)
    
