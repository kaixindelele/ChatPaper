# chatgpt 分析报告
## 接下来请逐文件分析下面的工程

## [0/13] 程序概述: get_paper.py

该文件是一个Python脚本，文件名为 get_paper.py，属于 ChatPaper 工程中的一个组成部分。它实现了一个 Paper 类和一个 main 函数。Paper 类代表了一篇论文，它可以从 PDF 文件中解析出论文的元信息和内容，并提供了一些函数用于获取论文信息，如获取文章标题，获取章节名称及内容等。主函数 main() 演示了如何使用 Paper 类处理 PDF 文件，根据 PDF 文件路径初始化 Paper 对象，并调用 parse_pdf() 函数解析 PDF 文件并获取相应的信息。

## [1/13] 程序概述: chat_arxiv_maomao.py

该程序文件名为 `chat_arxiv_maomao.py`，其功能为使用 OpenAI API 进行聊天和从 arxiv 搜索引擎中查询论文信息，并将相应的论文保存为PDF格式和部分信息保存为图片格式。程序文件使用了许多 Python 的第三方库，如 arxiv、numpy、openai、fitz 等。程序中定义了 `ArxivParams` 以及 `Paper`、`Reader` 三个类，其中 `ArxivParams` 定义了从 arxiv 搜索论文时需要的各种参数；`Paper` 类用于解析 PDF 文件，提取论文信息并保存为本地 PDF 文件及多个图片文件，其中包括论文标题、pdf 路径、每个章节标题对应的 pdf 页码、每个章节的正文内容、摘要信息，以及保存为图片文件的论文第一页；`Reader` 类主要用于在 arxiv 搜索引擎中查询论文信息，根据查询信息和关键词得到论文列表，再根据列表中的论文信息获取论文 pdf 文件并保存。

## [2/13] 程序概述: chat_paper.py

该程序文件名为chat_paper.py，包含一个Reader类和PaperParams元组。该程序功能为根据读者输入的搜索查询和感兴趣的关键词，从Arxiv数据库中获取文章，并对文章进行摘要和总结。程序使用了OpenAI的GPT-3模型生成文本摘要，使用了arxiv包获取Arxiv数据库中的文章。程序会将摘要和总结以markdown文件的形式保存下来。

Reader类包含了下载文章、筛选文章以及使用GPT-3生成文本摘要和总结的方法。主要方法有：

- get_arxiv(): 使用Arxiv的API获取搜索结果。
- filter_arxiv(): 筛选文章，并返回筛选后的结果。
- download_pdf(): 从Arxiv下载筛选后的文章。
- summary_with_chat(): 对每一篇下载下来的文章进行文本摘要和总结，并将结果以markdown文件的形式保存。

PaperParams元组包含了程序运行所需要的参数，如下载文件保存路径、搜索查询、关键词、排序方式、筛选关键词等。程序中使用了多次retry来保证程序的稳定性。

## [3/13] 程序概述: get_paper_from_pdf.py

本程序文件为Python脚本文件，文件名为get_paper_from_pdf.py，主要是通过调用fitz库和PIL库的方法，从PDF文件中解析出文章的各个部分的文本内容，包括标题、摘要、章节标题和正文等，并且对PDF文件中的图片进行提取和保存，并返回图片的路径和扩展名。

具体实现是定义了一个Paper类，通过传入PDF文件的路径初始化Paper对象，然后封装了一系列方法，如解析PDF文件的方法parse_pdf()，获取所有章节名称的方法get_chapter_names()，获取文章中的图片路径的方法get_image_path()等。最后在main()函数中调用了Paper类的parse_pdf()方法，并将解析出的各个部分的文本内容和图片路径打印输出。

## [4/13] 程序概述: app.py

该程序文件为一个基于 Flask 框架实现的 Web 应用程序，提供了四个功能模块：arxiv、 paper、 response 和 reviewer，分别对应搜索 Arxiv 上的论文、搜索并分析论文、处理论文审稿评论和查找论文审稿人四个功能。其中，每个功能模块定义了相应的路由函数，并使用 process_request 函数处理请求参数，并将请求参数作为参数调用相应的功能主函数，输出结果。此外，home 函数为应用的首页，提供了应用简介、各功能模块的描述以及该应用的 GitHub 项目地址等信息。最后，在程序结尾，代码根据命令行参数来启动应用程序。

## [5/13] 程序概述: chat_arxiv.py

这个程序的文件名是chat_arxiv.py。这个程序实现了一个论文下载器。在论文知识库 arXiv 上搜索论文，并下载相应的 PDF 文件。程序将会接收用户的查询字符串、关键词、搜索页数、文件格式等参数，为这些参数构建一个名为 ArxivParams 的元组。接着，程序使用提供的参数调用 arXiv API，获取查询到的论文列表。程序遍历每篇论文，并下载它们的 PDF 文件。程序接收到 PDF 后，使用 fitz 库打开它，提取出目录，正文和元数据等信息。在 PDF 中查找到第一张图片，并将它保存成 PNG 格式的文件。程序遍历文本，找到所有的章节名称和图片，并将它们保存成字典，并存储在 Paper 对象里。最后调用 Gitee API 将文件上传到 Gitee 仓库里。

## [6/13] 程序概述: chat_response.py

该程序文件是一个Python脚本，文件名为"chat_response.py"，主要功能是根据输入的评论文件路径，使用OpenAI的Chat API生成对应的回复文本，并将回复输出到指定格式的文件中。

具体包括以下功能：

1. 定义了一个Response类，包括了一些属性和方法，用于初始化和生成回复文本。

2. 定义了一个chat_response_main函数，用于启动Response类生成回复文本。

3. 通过导入argparse、configparser、datetime、json、os、re、time等模块，实现了参数解析、文件读写、时间处理、字符串匹配等操作。

4. 使用了numpy、openai、tenacity、tiktok等第三方库，实现了文本编码、OpenAI Chat API调用、重试机制、加密解密等功能。

5. 使用了正则表达式对文本进行匹配处理，提取关键信息后进行逻辑处理和字符串拼接，形成回复文本。

6. 实现输出格式为txt、markdown等格式的回复文件。

总之，该程序用于将审稿意见进行回复，实现了自动化生成回复文本的功能，从而提高了工作效率。

## [7/13] 程序概述: chat_reviewer.py

该程序文件是一个基于OpenAI Chat API的文献审稿系统，可以通过输入论文的标题、摘要、和各章节内容，生成相应的评审意见。主要包括以下内容：

1.导入所需要的模块和包

2.自定义namedtuple类ReviewerParams，包括4个属性：paper_path（论文路径），file_format（生成文件格式），research_fields（研究领域），language（输出语言）

3.自定义类Reviewer，包括以下方法：

  __init__: 初始化方法，用于设置属性

  validateTitle：用于校验论文的路径

  review_by_chatgpt：根据传入的论文列表，获取关键部分，发送至OpenAI Chat API，生成评审意见

  stage_1：审稿的第一阶段，根据传入的论文，提供标题、摘要、可提取的章节等信息并将其发送至OpenAI Chat API，以获取用户选择的章节

  chat_review：审稿的第二阶段，将用户选定的章节和关键部分发送至OpenAI Chat API，以生成审稿意见

  export_to_markdown：将审稿意见保存为markdown格式的文件

4.chat_reviewer_main：用于初始化程序，读取命令行参数后初始化Reviewer类，通过传入的论文路径或文件名，调用Reviewer类的review_by_chatgpt方法生成评审意见

该程序通过OpenAI Chat API调用人工智能模型，为用户提供便利的文献评审服务，同时又充分考虑到了对用户信息的保护，具有一定的可靠性和安全性。

## [8/13] 程序概述: google_scholar_spider.py

这个程序文件是一个可从 Google Scholar 网站上获取特定关键字相关论文信息的爬虫，主要用于研究学术领域的热点话题。该爬虫的主要功能包括：

1. 从命令行参数中获取关键字、结果数、CSV 文件路径、排序方式等信息；
2. 根据关键字和年份（可选）构建 Google Scholar 查询链接；
3. 使用 requests 库向链接发送请求，并对结果进行处理，包括获取标题、作者、被引用次数等；
4. 按照排序方式对结果进行排序，将结果保存为 CSV 文件，并可选择在结果中生成柱状图。

## [9/13] 程序概述: deploy/Public/app.py

该程序文件是一个Python脚本，文件名为app.py。该脚本包含了多个模块的导入和多个类和函数的定义。其中，一些重要的模块包括numpy、os、re、datetime、arxiv、openai、base64、requests、argparse、configparser、fitz、io、PIL、gradio、markdown、json、tiktoken、concurrent。主要的类包括Paper和Reader，辅助函数包括parse_text、api_key_check、valid_apikey、get_chapter_names、get_title、get_paper_info、get_image_path等。该程序还涉及到一些第三方API的调用，例如Arxiv、OpenAI等。该程序实现了一些功能，例如解析PDF文件，提取文本内容并按照章节组织成字典，获取PDF中每个页面的文本信息，根据字体大小识别每个章节名称等。该程序还可以检查有效的API密钥，生成一份有效的API密钥列表。

## [10/13] 程序概述: deploy/Public/optimizeOpenAI.py

该程序文件名为optimizeOpenAI.py，是一个官方ChatGPT API的简单包装器，主要实现了和ChatGPT模型的交互功能，包括对话、重置对话、获取对话摘要等，以及对于API调用时间、API key的管理和流程控制。其中提供了两个主要的方法：ask()用于获取model的回答信息，conversation_summary()用于获取对话的摘要信息。

## [11/13] 程序概述: deploy/Private/app.py

该程序实现了一个名为`chatPaper`的应用，用户可以通过输入特定的关键词，将获取的论文进行自动摘要和筛选，并使用OpenAI进行QA问答，由机器智能生成答案。其中，程序分为若干个子功能，包括：将PDF中的第一张图另存为图片，获取PDF文件中每个页面的文本信息并将其按章节组织成字典返回，获取PDF文件的标题，获取PDF文件中的章节。程序引入了numpy、os、re、datetime、arxiv、tenacity、base64、requests、argparse、configparser、PIL、gradio、fitz、io和optimizeOpenAI等库函数。主入口为`app.py`。

## [12/13] 程序概述: deploy/Private/optimizeOpenAI.py

这是一个名为optimizeOpenAI.py的程序文件,是一个对官方ChatGPT API的简单包装器。该文件定义了一个名为`chatPaper`的类，该类包含了用于与ChatGPT交互的各种方法。它使用OpenAI API完成交互，并在输入和输出之间维护存储对话的本地转换。它使用一个优先队列来存储API密钥，以确保API请求不会超过每个密钥的最大使用限制。在一个对话中，用户可以不断地提出问题并回答ChatGPT提供的管道中的问题。此外，该文件还包含用于重置对话、截断对话、计算并返回每个对话的当前令牌成本的函数，以及用于获取已注册的API密钥、检查API的可用性以及生成会话摘要的函数。

## 对程序的整体功能和构架做出概括。然后用一张markdown表格整理每个文件的功能（包括get_paper.py, chat_arxiv_maomao.py, chat_paper.py, get_paper_from_pdf.py, app.py, chat_arxiv.py, chat_response.py, chat_reviewer.py, google_scholar_spider.py, deploy/Public/app.py, deploy/Public/optimizeOpenAI.py, deploy/Private/app.py, deploy/Private/optimizeOpenAI.py）。

整体功能和构架概括：
ChatPaper是一个文献管理工具，主要针对学术论文的查询、下载、管理和评审等方面进行了自动化处理和优化，主要功能包括：
1. 论文的搜索和下载
2. 论文的摘要和评审自动生成
3. 论文的PDF文件解析和信息提取
4. 学术文献信息的爬取和整合
5. 学术论文开源代码的维护和管理


文件与功能对应表：

| 文件名 | 主要功能 |
| ------ | -------- |
| get_paper.py | 下载并解析PDF文件 |
| chat_arxiv_maomao.py | 在arxiv中搜索查询论文信息 |
| chat_paper.py | 搜索，下载，管理学术论文 |
| get_paper_from_pdf.py | 解析PDF文件 |
| app.py | 论文文献和爬虫 |
| chat_arxiv.py | 使用arxiv搜索引擎查询论文 |
| chat_response.py | 使用OpenAI API自动生成文献回复 |
| chat_reviewer.py | 使用OpenAI API自动生成评审建议 |
| google_scholar_spider.py | 从谷歌学术爬取论文摘要信息 |
| Public/app.py | 提取PDF信息 |
| Public/optimizeOpenAI.py | 自然语言处理概述 |
| Private/app.py | 学术论文查询和管理 |
| Private/optimizeOpenAI.py | OpenAI API请求处理 |

