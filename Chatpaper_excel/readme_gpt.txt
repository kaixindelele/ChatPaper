*****功能介绍：
这个程序将实现读取位于文件夹paper中的pdf
然后返回gpt对于论文的总结：这篇文献的标题，关键词，研究背景，研究方法，研究结论
上面这些内容将输出到文件夹paper_information
并将返回内容输出到excel

操作步骤：
1. 打开Main_readPaper.py
2. 输入密钥以及希望输入的excel文件名
3.运行Main_readPaper.py

一些程序介绍：
from readAbstract import GetFirstPage	获取论文首页
from OpenAI_readPaper import ReadPaper	问gpt论文核心
from output_paper_excel import OutputExcel	按格式追加到excel

output_Mpaper_message.py	使用chatgpt阅读多篇文献，并输出内容到txt
order_Pdf_File.py	假如论文是endnote导出的，可以一键将论文复制到文件夹Paper中
order_inf_to_excel.py	将论文信息输入到excel
Main_readPaper	主调用程序