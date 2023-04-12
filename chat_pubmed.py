## 正在写PubMed的爬虫，刚爬了一个title，先mark住，欢迎有时间的大佬按照arxiv的逻辑，把pubmed等其他的预印本爬虫写好~

import requests
from bs4 import BeautifulSoup

def crawl_pubmed_top_ten_papers_by_keywords(keywords):
    url = f"https://pubmed.ncbi.nlm.nih.gov/?term={'+'.join(keywords.split())}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.find_all("article", {"class": "full-docsum"})
    articles.sort(key=lambda x: x.find("span", {"class": "date"}).text.strip() if x.find("span", {"class": "date"}) else "")
    top_ten_articles = articles[:10]
    return top_ten_articles

if __name__ == "__main__":
    keywords = "cancer"
    top_ten_articles = crawl_pubmed_top_ten_papers_by_keywords(keywords)
    for i, article in enumerate(top_ten_articles):
        title = article.find("a", {"class": "docsum-title"}).text.strip()
        authors = article.find("span", {"class": "docsum-authors full-authors"}).text.strip() if article.find("span", {"class": "docsum-authors full-authors"}) else ""
        date = article.find("span", {"class": "date"}).text.strip() if article.find("span", {"class": "date"}) else ""
        print(f"{i+1}. {title}\n   {authors}\n   {date}\n")
