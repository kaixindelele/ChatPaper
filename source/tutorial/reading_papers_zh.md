# 使用 ChatPaper 阅读论文
在运行 `ChatPaper` 之前，您需要像下面代码块的示例一样，在 `apikey.ini` 的第 3 行中填写您的 OpenAI API 密钥。该密钥仅会保存在您的本地计算机上，因此使用起来是安全的。

```ini
...
OPENAI_API_KEYS = [sk-1234567890abcdefg] # 在此处输入您的 API 密钥
...
```


## 在命令行中运行 ChatPaper
`chat_paper.py` 脚本是运行 `ChatPaper` 的主要脚本。它可用于在 arXiv 上进行批量搜索，并下载相关论文并生成摘要。该脚本还可用于为本地 PDF 文件生成摘要。有关参数列表，请参见以下代码块：

```bash
用法: chat_paper.py [-h] [--pdf_path PATH] [--query QUERY] [--key_word KEYWORD]
                     [--language LANGUAGE] [--file_format FORMAT]
                     [--save_image SAVE_IMAGE] [--sort SORTCRITERIA]
                     [--max_results MAXRESULTS] [--filter_keys FILTERKEYS]
```
详细说明如下：
- `--pdf_path`：指定本地 PDF 文档的路径，供脚本读取。如果未设置，脚本将直接从 arXiv 搜索并下载。
- `--query`：ChatPaper 用于在 arXiv 上搜索论文的查询字符串。查询字符串可以是以下格式：`ti: xx, au: xx, all: xx,`，其中 `ti` 表示标题，`au` 表示作者，`all` 表示所有字段。例如，`ti: chatgpt, au: robot` 表示搜索标题包含 `chatgpt` 且作者包含 `robot` 的论文。有关查询字符串的更多信息，请参见以下表格：

| 前缀 | 描述 |
| --- | --- |
| ti | 标题 |
| au | 作者 |
| abs | 摘要 |
| co | 评论 |
| jr | 期刊引用 |
| cat | 主题类别 |
| rn | 报告编号 |
| id | ID（请改用 `id_list`） |
| all | 以上所有 |

- `--key_word`：用户研究领域的关键词。该参数用于过滤与用户研究领域无关的论文。例如，如果用户对强化学习感兴趣，他/她可以将 `--key_word` 设置为 `reinforcement learning`，这样 ChatPaper 将只总结与强化学习相关的论文。
- `--language`：摘要的语言。目前，ChatPaper 支持两种语言：中文和英文。默认语言为中文。要使用英文，请将 `--language` 设置为 `en`。
- `--file_format`：导出文件的格式。目前，ChatPaper 支持两种格式：Markdown 和纯文本。默认格式为 Markdown。要使用纯文本，请将 `--file_format` 设置为 `txt`。
- `--save_image`：是否保存论文中的图片。保存一张图片需要一两分钟的时间。
- `--sort`：搜索结果的排序标准。目前，ChatPaper 支持两种排序标准：相关性和最后更新日期。默认排序标准为相关性。要使用最后更新日期，请将 `--sort` 设置为 `LastUpdatedDate`。
- `--max_results`：结果的最大数量。默认值为 1。
- `--filter_keys`：过滤关键词。ChatPaper 仅会总结摘要中包含所有过滤关键词的论文。例如，如果用户对强化学习感兴趣，他/她可以将 `--filter_keys` 设置为 `reinforcement learning`，这样 ChatPaper 将只总结摘要中包含 `reinforcement learning` 的论文。
  
在接下来的部分，我们将列出 ChatPaper 的命令行用法。

- 使用 ChatPaper 在 arXiv 上进行批量搜索，并下载相关论文并生成摘要

```bash
python chat_paper.py --query "chatgpt robot" --filter_keys "chatgpt robot" --language "en" --max_results 3
```

上述命令将在 arXiv 上搜索与 "chatgpt robot" 相关的论文，下载论文，并为每篇论文生成摘要。下载的 PDF 文件将保存在 `./pdf_files` 文件夹中，摘要将保存在 `./export` 文件夹中。

更准确的脚本是 `chat_arxiv.py`，示例命令行用法如下：

```bash
python chat_arxiv.py --query "chatgpt robot" --page_num 2 --max_results 3 --days 10
```

这里，`query` 仍然是关键字，`page_num` 是搜索页面，每页最多 50 篇文章，就像 arXiv 网站上一样。`max_results` 是要总结的文章数，`days` 是要搜索的天数。默认参数与上面相同。

*注意：*搜索术语不能识别 "-"，而只能识别空格。因此最好不要在原始标题中使用连字符。

- 使用 ChatPaper 在 arXiv 上进行*高级*批量搜索，并下载相关论文并生成摘要

```bash
python chat_paper.py --query "all: reinforcement learning robot 2023" --filter_keys "reinforcement robot" --max_results 3
```

- 使用 ChatPaper 在 arXiv 上进行*高级*批量搜索*特定作者*，并下载相关论文并生成摘要

```bash
python chat_paper.py --query "au: Sergey Levine" --filter_keys "reinforcement robot" --max_results 3
```

- 本地 PDF 摘要
```bash
python chat_paper.py --pdf_path "demo.pdf"
```

- 本地 PDF 摘要（批量）
```bash
python chat_paper.py --pdf_path "absolute_path_to_paper_folder"
```

*注意：*ChatPaper 目前仅支持非综述论文。

---

你还可以使用 `google_scholar_spider.py` 脚本在 Google Scholar 上进行批量搜索。例如，你可以使用以下命令在 Google Scholar 上搜索与 "deep learning" 相关的论文，并将结果保存到 `CSV` 文件中：

```bash
python google_scholar_spider.py --kw "deep learning" --nresults 30 --csvpath "./data" --sortby "cit/year" --plotresults 1
```

这个命令在 Google Scholar 上搜索与 "deep learning" 相关的论文，检索 30 个结果，将结果保存到 `./data` 文件夹中的 `CSV` 文件中，按每年的引用排序，并绘制结果。

请参考 [https://github.com/JessyTsu1/google_scholar_spider](https://github.com/JessyTsu1/google_scholar_spider) 了解具体用法和参数。


## 在浏览器中运行 ChatPaper
本功能依托于 `Flask` 库。首先，安装虚拟环境工具并创建一个名为 `venv` 的新虚拟环境：

```bash
pip install virtualenv
virtualenv venv
```

然后，激活虚拟环境。

在 Linux/Mac 上：
```bash
source venv/bin/activate
```

在 Windows 上：
```powershell
.\venv\Scripts\activate.bat
```

最后，启动服务。

```bash
python app.py
```

运行此命令后，`Flask` 服务将在端口 5000 上启动并等待用户请求。在浏览器中访问以下 URL 之一即可访问 Flask 服务的主页：

```
http://127.0.0.1:5000/
或者
http://127.0.0.1:5000/index
```

在访问 [http://127.0.0.1:5000/](http://127.0.0.1:5000/) 之后，您将看到主页。在主页上，您可以单击不同的链接来调用各种服务。通过修改链接中的参数值，您可以实现不同的效果。

主页上的四个链接是：
- `arxiv`。它调用根目录中的 `chat_arxiv.py` 脚本在 *arXiv* 上搜索论文并生成摘要。参数与 `chat_arxiv.py` 脚本相同。
- `paper`。它调用根目录中的 `chat_paper.py` 脚本为 *本地* PDF 文件生成摘要。参数与 `chat_paper.py` 脚本相同。
- `response`。它调用根目录中的 `chat_response.py` 脚本为期刊/会议论文审稿生成回复。您应该将审稿意见准备在 *本地* 文本文件中。对于参数，它有：
  - `--comment_path`：要回复的审稿文本文件的路径
  - `--language`：您的回复语言。目前，ChatPaper 支持两种语言：英语和中文。要使用英语，只需将 `--language` 设置为 `en`。
- `reviewer`。它调用根目录中的 `chat_reviewer.py` 脚本为期刊/会议论文审稿生成审稿人意见。您应该将审稿意见准备在 *本地* 文本文件中。对于参数，它有：
  - `--paper_path`：要回复的审稿文本文件的路径
  - `--research_field`：论文的研究领域。目前，ChatPaper 支持两种语言：英语和中文。要使用中文，只需将 `--language` 设置为 `zh`。

这四个接口实际上是封装了根目录中的四个脚本的 Web 接口。可以通过链接修改参数。例如，如果要运行 `arxiv?query=GPT-4&key_word=GPT+robot&page_num=1&max_results=1&days=1&sort=web&save_image=False&file_format=md&language=zh`，则等效于在根目录中调用 `chat_arxiv.py` 并返回结果。显示的结果与通过命令行调用脚本（即 `python chat_arxiv.py --query "GPT-4" --key_word "GPT robot" --page_num 1 --max_results 1 --days 1 --sort "web" --save_image False --file_format "md" --language "zh"`）获得的结果相同。您可以通过修改参数来获得其他搜索结果。

如果您使用这种方式中运行 ChatPaper，生成的结果将会保存在同一目录下新生成的 `export`、`pdf_files` 和 `response_file` 文件夹中。

## 在 Docker 中运行 ChatPaper

首先，在您的计算机上安装 Docker。请参考 [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/) 了解具体安装方法。

然后，将 `docker-compose.yml` 文件放在您想要在其中运行 ChatPaper 的任何目录中。然后，修改 `docker-compose.yml` 文件的第 21 行，将您的 OpenAI API 密钥输入如下：

```bash
...
environment:
      - OPENAI_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx # 在这里输入您的密钥
...
```

最后，在 `docker-compose.yml` 文件所在的目录中运行以下命令：

```bash
docker-compose up -d
```

运行此命令后，docker 容器将在 [https://127.0.0.1:28460/](https://127.0.0.1:28460/) 上启动并等待用户请求。

此外，如果您有任何想法来改进项目，您可以查看 `build.sh`、`dev.sh` 和 `tagpush.sh` 脚本的功能，以及根目录中的 docker 目录中的文件。我们相信它们将进一步增强您对容器化项目封装的理解。

所有生成的结果都保存在 Docker 卷中。如果您想将它们部署为长期服务，可以映射这些目录。默认情况下，它们位于 `/var/lib/docker/volumes/` 中。您可以进入此目录并在四个相关文件夹中查看结果：`chatpaper_log`、`chatpaper_export`、`chatpaper_pdf_files` 和 `chatpaper_response_file`。有关 Docker 卷的更详细的解释，请参考此链接：[http://docker.baoshu.red/data_management/volume.html](http://docker.baoshu.red/data_management/volume.html)。

## 在 Hugging Face 中运行 ChatPaper

首先，注册并登录到 [Hugging Face Hub](https://huggingface.co/)。

其次，进入 ChatPaper 的主要仓库：[https://huggingface.co/spaces/wangrongsheng/ChatPaper](https://huggingface.co/spaces/wangrongsheng/ChatPaper)。您可以在 "Files and Version" 部分看到所有最新的部署代码。

对于私有部署，您可以点击 "Duplicate this space"，在弹出的页面中选择 Visibility 为 "Private"。最后，点击 "Duplicate Space"，Space 代码将部署到您自己的空间中。为了让您在每次调用时不用填写 API 密钥，您可以修改 `app.py` 的第 845 行，将其改为您自己的密钥：`default="sk-abcdxxxxxxxx"`，然后点击保存以立即重新部署；

对于公共部署，您可以点击 "Duplicate this space"，在弹出的页面中选择 Visibility 为 "Public"。最后，点击 "Duplicate Space"，Space 代码将部署到您自己的空间中，从而形成公共部署。

您可以根据需要选择公共或私有部署。
