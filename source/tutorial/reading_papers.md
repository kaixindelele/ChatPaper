# Using ChatPaper to read papers

Before running ChatPaper, you need to fill in your OpenAI API key in line 3 of `apikey.ini`. The key would only stay in your local machine so it is safe to use.

For instance, it would done as follows:
```ini
OPENAI_API_KEYS = [sk-1234567890abcdefg] # input your API key here
```

## Running ChatPaper in command line

The `chat_paper.py` script is the main script for running ChatPaper. It can be used to perform batch search on arXiv and download related papers and generate a summary. The script can also be used to generate a summary for a local PDF file. For list of arguments, please refer to the following codeblock:


```bash
usage: chat_paper.py [-h] [--pdf_path PATH] [--query QUERY] [--key_word KEYWORD]
                     [--language LANGUAGE] [--file_format FORMAT]
                     [--save_image SAVE_IMAGE] [--sort SORTCRITERIA]
                     [--max_results MAXRESULTS] [--filter_keys FILTERKEYS]
```

Detailed usage of each argument is as follows:

- `--pdf_path`: Specifing the path for local PDF documents for the script to read. If not set, the script will search and download from arXiv directly.
- `--query`: the query string used by ChatPaper to search for papers on arXiv. The query string can be in the following format: `ti: xx, au: xx, all: xx,` where `ti` stands for title, `au` stands for author, and `all` stands for all fields. For instance, `ti: chatgpt, au: robot` means searching for papers with title containing `chatgpt` and author containing `robot`.
- `--key_word`: the key word of user research fields. This argument is used to filter out papers that are not related to the user's research fields. For instance, if the user is interested in reinforcement learning, he/she can set `--key_word` to `reinforcement learning` so that ChatPaper will only summarize papers related to reinforcement learning.
- `--language`: the language of the summary. Currently, ChatPaper supports two languages: Chinese and English. The default language is Chinese. To use English, simply set `--language` to `en`.
- `--file_format`: the format of the exported file. Currently, ChatPaper supports two formats: Markdown and plain text. The default format is Markdown. To use plain text, simply set `--file_format` to `txt`.
- `--save_image`: whether to save the images in the paper. It takes a minute or two to save a picture! 
- `--sort`: the sorting criteria of the search results. Currently, ChatPaper supports two sorting criteria: relevance and last updated date. The default sorting criteria is relevance. To use last updated date, simply set `--sort` to `LastUpdatedDate`.
- `--max_results`: the maximum number of results. The default value is 1.
- `--filter_keys`: the filter key words. ChatPaper will only summarize papers that contain all the filter key words in their abstracts. For instance, if the user is interested in reinforcement learning, he/she can set `--filter_keys` to `reinforcement learning` so that ChatPaper will only summarize papers related to reinforcement learning.

We would list the command-line usage of ChatPaper in the following lists.

- Using ChatPaper to perform batch search on arXiv and download related papers and generate a summary

```bash
python chat_paper.py --query "chatgpt robot" --filter_keys "chatgpt robot" --language "en" --max_results 3
```
The above command will search for papers related to "chatgpt robot" on arXiv, download the papers, and generate a summary for each paper. The downloaded PDF files would be saved in `./pdf_files` folder and the summary will be saved in the `./export` folder.

A more accurate script is `chat_arxiv.py`, sample command line usage is as follows:

```bash
python chat_arxiv.py --query "chatgpt robot" --page_num 2 --max_results 3 --days 10
```

Here, `query` is still the keyword, `page_num` is the search page, with a maximum of 50 articles per page like on the arXiv site. `max_results` is the number of articles to summarize, and `days` is the number of recent days to select papers from. The default parameters are the same as above.

*Note:* the search term cannot recognize "-", but only space. So it is best not to use hyphens in the original title.

- Using ChatPaper to perform *advanced* batch search on arXiv and download related papers and generate a summary

```bash
python chat_paper.py --query "all: reinforcement learning robot 2023" --filter_keys "reinforcement robot" --max_results 3
```
- Using ChatPaper to perform *advanced* batch search *of a specific author* on arXiv and download related papers and generate a summary

```bash
python chat_paper.py --query "au: Sergey Levine" --filter_keys "reinforcement robot" --max_results 3
```

- Local PDF summary
```bash
python chat_paper.py --pdf_path "demo.pdf"
```

- Local *Batch* PDF summary

```bash
python chat_paper.py --pdf_path "absolute_path_to_paper_folder"
```



*Note:* The script currently only supports non-survey papers.

---

You can also perform a paper survey via Google Scholar by running:

```bash
python google_scholar_spider.py --kw "deep learning" --nresults 30 --csvpath "./data" --sortby "cit/year" --plotresults 1
```

This command searches for articles related to "deep learning" on Google Scholar, retrieves 30 results, saves the results to a CSV file in the `./data` folder, sorts the data by citation per year, and plots the results.

Please refer to [https://github.com/JessyTsu1/google_scholar_spider](https://github.com/JessyTsu1/google_scholar_spider) for specific usage and parameters.

## Running ChatPaper in Flask

First, install the virtual environment tool and create a new virtual environment named `venv`:

```bash
pip install virtualenv
virtualenv venv
```

Then, activate the virtual environment.

On Linux/Mac:
```bash
source venv/bin/activate
```

On Windows:
```powershell
.\venv\Scripts\activate.bat
```

Finally, start the service.

```bash
python app.py
```
After running this command, the Flask service will start on port 5000 and wait for user requests. Visit one of the following URLs in your browser to access the main page of the Flask service:

```
http://127.0.0.1:5000/
or
http://127.0.0.1:5000/index
```

After visiting [http://127.0.0.1:5000/](http://127.0.0.1:5000/), you will see the main page. On the main page, you can click on different links to call various services. You can achieve different effects by modifying the parameter values in the links. 

The four links on the main page are:
- arxiv. It calls the `chat_arxiv.py` script in the root directory to search for papers on *arXiv* and generate a summary. The parameters are the same as those of the `chat_arxiv.py` script.
- paper. It calls the `chat_paper.py` script in the root directory to generate a summary for a *local* PDF file. The parameters are the same as those of the `chat_paper.py` script.
- response. It calls the `chat_response.py` script in the root directory to generate a response for a journal/conference paper review. The review you should prepare in a *local* text file. For the parameters, it has:
  - `--comment_path`: the path of the review text file should be respond to
  - `--language`: the language of your response. Currently, ChatPaper supports two languages: English and Chinese. To use English, simply set `--language` to `en`.
  
- reviewer. It calls the `chat_reviewer.py` script in the root directory to generate a review for a *local* PDF file in the format of journals/conference reviewer. For the parameters, it has:
  - `--paper_path`: the path of the PDF file should be reviewed
  - `--research_fields`: the research fields of the paper
  - `--language`: the language of your response. Currently, ChatPaper supports two languages: English and Chinese. To use English, simply set `--language` to `en`.

The four interfaces are actually web interfaces that encapsulate the four scripts in the root directory. Parameters can be modified through the links. For example, if you want to run `arxiv?query=GPT-4&key_word=GPT+robot&page_num=1&max_results=1&days=1&sort=web&save_image=False&file_format=md&language=zh`, it is equivalent to calling `chat_arxiv.py` in the root directory and returning the results. The displayed results are the same as those obtained by calling the script on the command line (i.e. `python chat_arxiv.py --query "GPT-4" --key_word "GPT robot" --page_num 1 --max_results 1 --days 1 --sort "web" --save_image False --file_format "md" --language "zh"`). You can obtain other search results by modifying the parameters.

If you deploy the project in this way, the results will be saved in the newly generated `export`, `pdf_files`, and `response_file` folders in the same directory.

## Running ChatPaper in Docker

First, install Docker on your computer. Please refer to [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/) for specific installation methods.

Then, place `docker-compose.yml` file in whatever directory you want to run ChatPaper in. Then, modify line 21 of `docker-compose.yml` file to input your OpenAI API key as follows:

```bash
...
environment:
      - OPENAI_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx # Your key here
...
```

Finally, run the following command in the directory where `docker-compose.yml` is located:

```bash
docker-compose up -d
```

After running this command, the docker container will start and wait for user requests on [https://127.0.0.1:28460/](https://127.0.0.1:28460/).

In addition, if you have any ideas to improve the project, you can check the functions of the `build.sh`, `dev.sh`, and `tagpush.sh` scripts, as well as the files in the docker directory in the root directory. We believe that they will further enhance your understanding of containerized project encapsulation.

All results are saved in Docker volumes. If you want to deploy them as a long-term service, you can map these directories. By default, they are located in `/var/lib/docker/volumes/`. You can enter this directory and view the results in the four related folders: `chatpaper_log`, `chatpaper_export`, `chatpaper_pdf_files`, and `chatpaper_response_file`. For more detailed explanations of Docker volumes, please refer to this link: [http://docker.baoshu.red/data_management/volume.html](http://docker.baoshu.red/data_management/volume.html).

## Running ChatPaper in Hugging Face
First, create your own Hugging Face account and log in to the [Hugging Face Hub](https://huggingface.co/). 

Then, go to the ChatPaper main repository: [https://huggingface.co/spaces/wangrongsheng/ChatPaper](https://huggingface.co/spaces/wangrongsheng/ChatPaper). You can see all the latest deployment code in the "Files and Version" section.

*Optional:* For private deployment, click on "Duplicate this space" and in the pop-up page, select Visibility as "Private". Finally, click "Duplicate Space", and the Space code will be deployed to your own space. To make it more convenient for you to call without filling in the API key each time, you can modify line 845 of `app.py` with your own key: `default="sk-abcdxxxxxxxx"`, and click save to immediately redeploy;

*Optional:* For public deployment, click on "Duplicate this space" and in the pop-up page, select Visibility as "Public". Finally, click "Duplicate Space", and the Space code will be deployed to your own space, making it a public deployment.

Note: You can choose either public or private deployment based on your needs!