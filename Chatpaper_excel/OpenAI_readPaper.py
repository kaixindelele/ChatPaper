import openai
import tenacity

#中文输出
def ReadPaper_c(content, openaikey):
    openai.api_key = openaikey
    text=content
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一个科研人员，善于使用精炼的语句总结论文"},  # chatgpt 角色
            {"role": "assistant", "content": "这是一篇英文文献的首页，我需要你帮忙阅读并归纳一些问题："+text},  # 背景知识
            {"role": "user", "content": "使用中文回答（专有名词可以不用中文)，语句尽量简洁且学术，不要照搬摘要，可适当扩展。请问这篇文献的标题，关键词，研究背景，研究方法，研究结论分别是什么? \n 按照后面的格式输出: Title: xxx\n\nKeywords: xxx\n\nResearch Background: xxx\n\nResearch Methods: xxx\n\nResearch Conclusion: xxx。务必严格按照格式，使用中文回答，将对应内容输出到xxx中，不要输出多余的内容"},  # 问问题
        ]
    )
    result = ''
    for choice in response.choices:
        result += choice.message.content
    return(result)
# Use tenacity to retry with exponential backoff
@ tenacity.retry(
    wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
    stop=tenacity.stop_after_attempt(5),
    reraise=True,
)
#英文输出
def ReadPaper_e(content, openaikey):
    openai.api_key = openaikey
    text=content
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a research scientist and you are skilled at summarizing academic papers using concise language."},  # chatgpt 角色
            {"role": "assistant", "content": "This is the first page of a research paper, and I need your help to read and summarize some questions ："+text},  # 背景知识
            {"role": "user", "content": "Please answer in English and use concise and acdemic language. Do not simply copy and paste the abstract, but you can expand it appropriately. What are the title, keywords,research background, research methods, and research conclusion of this literature? \n Output in the format——Title: xxx\n\nKeywords: xxx\n\nResearch Background: xxx\n\nResearch Methods: xxx\n\nResearch Conclusion: xxx. Please strictly follow the format and do not output any extra content."},  # 问问题
        ]
    )
    result = ''
    for choice in response.choices:
        result += choice.message.content
    return(result)
