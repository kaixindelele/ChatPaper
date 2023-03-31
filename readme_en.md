# ChatPaper

<div style="font-size: 1.5rem;">
  <a href="./README.md">中文</a> |
  <a href="./readme_en.md">English</a>
</div>
</br>

💥💥💥The free web version of ChatPaper, which is open to the world and serves thousands of researchers, is officially launched:[https://chatpaper.org/](https://chatpaper.org/) 💥💥💥


To keep up with the huge ArXiv papers and AI’s fast progress, we humans need to evolve. We download the latest papers on arxiv based on user keywords, and use ChatGPT3.5 API’s powerful summarization to condense them into a fixed format with minimal text and easy readability. 
We provide the most information for everyone to choose which papers to read deeply.

## TODO list:
1. Change all prompts to English.  --completed!
2. Use a more robust method to parse the Method section.
3. If there is a brother who wants to build a website, we can cooperate. --completed!
4. Implement a ChatReview version for everyone to refer to when reviewing (but there may be academic ethics issues?)
5. Output English mode! just set lauguage as "en"!

## Motivation

Facing the massive arXiv papers every day, and AI's rapid evolution, we humans must also evolve together in order not to be eliminated.

As a PhD student in Reinforcement Learning at USTC, I feel anxious. My brain holes can even not keep up with the speed of AI evolution now.

Therefore I developed this **ChatPaper**, trying to use magic to defeat magic.

**ChatPaper is a paper summary tool**: AI summarizes papers in one minute, and users read papers summarized by AI in one minute.

It can automatically download the latest papers from arXiv based on the keywords entered by the user, and then use ChatGPT3.5's powerful API interface summary ability to summarize the paper into a fixed format, with minimal text and lowest reading threshold to provide you with maximum information volume to decide which articles should be read carefully.

You can also provide local PDF document addresses for direct processing.

Generally speaking, you can quickly pass through a small field of latest articles in one night. I have tested it for two days myself.

I wish everyone can evolve with AI in this rapidly changing era!

Although this code is not much, it took me nearly a week to get through the whole process and share it with you today.

Your support is the motivation for my continuous update!

<div style="text-align: center;">
  <img src=https://user-images.githubusercontent.com/28528386/224465754-6f886e48-8626-419f-a154-e5d187fd22f9.jpg width="200" height="250"/>
</div>

<div style="text-align: center;">
  <img src=https://user-images.githubusercontent.com/28528386/224335122-1e87eb7b-a922-4c2f-b2aa-9612f62a6314.jpg width="200" height="250"/>
</div>


## How to use:
### 一、Run with python scripts

Windows, MAC and Ubuntu systems should be fine;

python version is best 3.9, other versions should not have any problems

1. Fill in your openai key in apikey.ini. Note that this code is a pure local project, your key is very safe!

2. The process must ensure global proxy! (Non-Chinese users may not have this problem)

3. Install dependencies:
``` bash
pip install -r requirements.txt
```
4. Run chat_paper.py, for example:

```python
python chat_paper.py --query "chatgpt robot" --filter_keys "chatgpt robot" --max_results 1 --language en
```

5. Parameter introduction:
```
[--pdf_path Whether to directly read local pdf documents? If not set, download directly from arxiv with query] 
[--query The keywords searched on the arxiv website, some abbreviations are demonstrated: all, ti(title), au(author), an example query: all: ChatGPT robot] 
[--key_word The keywords of your interested field, not very important] 
[--filter_keys The keywords you need to search in the abstract text, each word must appear to be your target paper] 
[--max_results The maximum number of articles searched each time, after the above filtering, it is your target number of papers, chat only summarizes filtered papers] 
[--sort arxiv sorting method, default is relevance, can also be time , arxiv.SortCriterion.LastUpdatedDate or arxiv.SortCriterion.Relevance , don't add quotation marks] 
[--save_image Whether to save pictures , if you haven't registered gitee's picture bed , default is false ] 
[--file_format File save format , default is markdown's md format , can also be txt ] 
```

### 二、Run with Flask web server

1. Download the project and enter the project directory

```
textCopy code
git clone https://github.com/kaixindelele/ChatPaper.git
cd ChatPaper
```

2. Fill in your OpenAI key in the `apikey.ini` file in the project root directory.

3. Set up the virtual environment and install the required dependencies

```
textCopy code
pip install virtualenv 
# Install the virtual environment tool
virtualenv venv 
# Create a new virtual environment named venv
For Linux/Mac:
source venv/bin/activate

For Windows:
.\venv\Scripts\activate.bat

pip install -r requirements.txt
# Install the required dependencies for the project
```

4. Start the service

```
textCopy code
python3 app.py
# Start the Flask service. After running this command, the Flask service will start on the local port 5000 and wait for user requests. Access the Flask service homepage by visiting one of the following addresses in your browser:
# http://127.0.0.1:5000/
# or
# http://127.0.0.1:5000/index
```

After visiting http://127.0.0.1:5000/, you will see the homepage. On the homepage, you can click on different links to call various services. You can achieve different effects by modifying the parameter values in the links. For detailed information about the parameters, please refer to the instructions in step above.



### 三、Running with Docker

1. Install Docker and Docker Compose by following the links below:

   https://yeasy.gitbook.io/docker_practice/install

   https://yeasy.gitbook.io/docker_practice/compose/install

2. Place the "docker-compose.yaml" file from the project's root directory in a suitable location, and replace `YOUR_KEY_HERE` with your own OpenAI key on line 21.

3. Run the following command in the command line in the same directory:

   ```
   docker-compose up -d
   ```

4. If the interface looks like this, everything is working properly, and you can access it from a web page by visiting [https://127.0.0.1:28460](https://127.0.0.1:28460/)! ![docker-compose](/Users/jessytsui/PycharmProjects/ChatPaper/images/docker-compose.png)

+ If you have any ideas for improving the project, you can take a look at the functions of the "build.sh," "dev.sh," "tagpush.sh" scripts, and the files in the "docker" directory at the root level. We believe they will help you further enhance your ideas on containerization and project encapsulation.

  

## Tips for using the project:

Quickly brush papers with specific keywords, without illustrations, each article takes a minute, reading time is about a minute.

This project can be used to track the latest papers in a field, or pay attention to papers in other fields, can batch generate summaries, up to 1000 (if you can wait).
Although Chat may have some nonsense elements, but under my standardized questioning framework, its main information is valuable.

The digital parts need everyone to go back to check in the original text!

After finding a good article, you can read this article carefully.

Recommend two other AI-assisted websites for reading papers: https://typeset.io/ and chatpdf.
My tutorial: [Reinforcement Apprentice: Paper Reading Artifact SciSpace(Typeset.io) Evaluation-Evolve with AI](https://zhuanlan.zhihu.com/p/611874187)

The main advantage over these two tools is that ChatPaper can automatically summarize the latest papers in batches, which can greatly reduce the reading threshold, especially for us Chinese.
The disadvantage is also obvious. ChatPaper has no interactive function and cannot ask questions continuously. But I think this is not very important~


## Summary Demo:

![6O4E3VW~X (7I }`ZV`Z`J](https://user-images.githubusercontent.com/28528386/224890637-62be8d42-813c-40ff-8c69-90bb13080e21.png)
