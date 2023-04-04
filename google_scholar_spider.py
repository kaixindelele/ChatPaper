import argparse
import datetime
import os
import sys
import time
import warnings
from dataclasses import dataclass
from time import sleep
from typing import List, Optional

import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

now = datetime.datetime.now()
current_year = now.year
MAX_CSV_FNAME = 255

# Websession Parameters
GSCHOLAR_URL = 'https://scholar.google.com/scholar?start={}&q={}&hl=en&as_sdt=0,5'
YEAR_RANGE = ''  # &as_ylo={start_year}&as_yhi={end_year}'
# GSCHOLAR_URL_YEAR = GSCHOLAR_URL+YEAR_RANGE
STARTYEAR_URL = '&as_ylo={}'
ENDYEAR_URL = '&as_yhi={}'
ROBOT_KW = ['unusual traffic from your computer network', 'not a robot']


@dataclass
class GoogleScholarConfig:
    keyword: str = "machine learning"
    nresults: int = 50
    save_csv: bool = True
    csvpath: str = "."
    sortby: str = "Citations"
    plot_results: bool = False
    start_year: Optional[int] = None
    end_year: int = current_year
    debug: bool = False


def google_scholar_spider(GoogleScholarConfig: GoogleScholarConfig):
    # Create main URL based on command line arguments
    gscholar_main_url = create_main_url(GoogleScholarConfig)

    # Start new session
    session = requests.Session()

    # data = fetch_data(GoogleScholarConfig, session, gscholar_main_url)
    with tqdm(total=GoogleScholarConfig.nresults) as pbar:
        # Call fetch_data() with pbar argument
        data = fetch_data(GoogleScholarConfig, session, gscholar_main_url, pbar)

    # Create a dataset and sort by the number of citations
    data_ranked = process_data(data, GoogleScholarConfig.end_year, GoogleScholarConfig.sortby)

    # Plot by citation number
    if GoogleScholarConfig.plot_results:
        plot_results(data_ranked.index, data_ranked["Citations"], GoogleScholarConfig.keyword)

    # Save results
    if GoogleScholarConfig.save_csv:
        save_data_to_csv(data_ranked, GoogleScholarConfig.csvpath, GoogleScholarConfig.keyword)


def get_command_line_args() -> GoogleScholarConfig:
    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument('--kw', type=str,
                        help="""Keyword to be searched. Use double quote followed by simple quote to search for an exact keyword. Example: "'exact keyword'" """)
    parser.add_argument('--sortby', type=str,
                        help='Column to be sorted by. Default is by the columns "Citations", i.e., it will be sorted by the number of citations. If you want to sort by citations per year, use --sortby "cit/year"')
    parser.add_argument('--nresults', type=int,
                        help='Number of articles to search on Google Scholar. Default is 100. (carefull with robot checking if value is too high)')
    parser.add_argument('--csvpath', type=str,
                        help='Path to save the exported csv file. By default it is the current folder')
    parser.add_argument('--notsavecsv', action='store_true',
                        help='By default results are going to be exported to a csv file. Select this option to just print results but not store them')
    parser.add_argument('--plotresults', action='store_true',
                        help='Use this flag in order to plot the results with the original rank in the x-axis and the number of citaions in the y-axis. Default is False')
    parser.add_argument('--startyear', type=int, help='Start year when searching. Default is None')
    parser.add_argument('--endyear', type=int, help='End year when searching. Default is current year')
    parser.add_argument('--debug', action='store_true',
                        help='Debug mode. Used for unit testing. It will get pages stored on web archive')

    args, _ = parser.parse_known_args()

    return GoogleScholarConfig(
        keyword=args.kw if args.kw else GoogleScholarConfig.keyword,
        nresults=args.nresults if args.nresults else GoogleScholarConfig.nresults,
        save_csv=not args.notsavecsv,
        csvpath=args.csvpath if args.csvpath else GoogleScholarConfig.csvpath,
        sortby=args.sortby if args.sortby else GoogleScholarConfig.sortby,
        plot_results=args.plotresults,
        start_year=args.startyear if args.startyear else GoogleScholarConfig.start_year,
        end_year=args.endyear if args.endyear else GoogleScholarConfig.end_year,
        debug=args.debug
    )


def get_citations(content):
    citation_start = content.find('Cited by ')
    if citation_start == -1:
        return 0
    citation_end = content.find('<', citation_start)
    return int(content[citation_start + 9:citation_end])


def get_year(content):
    for char in range(0, len(content)):
        if content[char] == '-':
            out = content[char - 5:char - 1]
    if not out.isdigit():
        out = 0
    return int(out)


def setup_driver():
    try:
        from selenium import webdriver
        from selenium.common.exceptions import StaleElementReferenceException
        from selenium.webdriver.chrome.options import Options
    except Exception as e:
        print(e)
        print("Please install Selenium and chrome webdriver for manual checking of captchas")

    # print('Loading...')
    chrome_options = Options()
    chrome_options.add_argument("disable-infobars")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver


def get_author(content):
    author_end = content.find('-')
    return content[2:author_end - 1]


def get_element(driver, xpath, attempts=5, count=0):
    '''Safe get_element method with multiple attempts'''
    try:
        element = driver.find_element_by_xpath(xpath)
        return element
    except Exception as e:
        if count < attempts:
            sleep(1)
            get_element(driver, xpath, attempts=attempts, count=count + 1)
        else:
            print("Element not found")


def get_content_with_selenium(url):
    global driver
    if 'driver' not in globals():
        driver = setup_driver()

    driver.get(url)
    el = get_element(driver, "/html/body")
    content = el.get_attribute('innerHTML')

    if any(kw in content for kw in ROBOT_KW):
        input("Solve captcha manually and press enter here to continue...")
        driver.get(url)
        el = get_element(driver, "/html/body")
        content = el.get_attribute('innerHTML')

    return content.encode('utf-8')


def create_main_url(GoogleScholarConfig: GoogleScholarConfig) -> str:
    if GoogleScholarConfig.start_year:
        gscholar_main_url = GSCHOLAR_URL + STARTYEAR_URL.format(GoogleScholarConfig.start_year)
    else:
        gscholar_main_url = GSCHOLAR_URL

    if GoogleScholarConfig.end_year != current_year:
        gscholar_main_url = gscholar_main_url + ENDYEAR_URL.format(GoogleScholarConfig.end_year)

    if GoogleScholarConfig.debug:
        gscholar_main_url = 'https://web.archive.org/web/20210314203256/' + GSCHOLAR_URL

    return gscholar_main_url


def fetch_data(GoogleScholarConfig: GoogleScholarConfig, session: requests.Session, gscholar_main_url: str,
               pbar: None) -> pd.DataFrame:
    links: List[str] = []
    title: List[str] = []
    citations: List[int] = []
    year: List[int] = []
    author: List[str] = []
    venue: List[str] = []
    publisher: List[str] = []
    rank: List[int] = [0]

    # Initialize progress bar
    if pbar is not None:
        pbar.reset(total=GoogleScholarConfig.nresults)

    # Get content from number_of_results URLs
    for n in range(0, GoogleScholarConfig.nresults, 10):

        if pbar is not None:
            pbar.update(10)

        url = gscholar_main_url.format(str(n), GoogleScholarConfig.keyword.replace(' ', '+'))
        if GoogleScholarConfig.debug:
            print("Opening URL:", url)

        # print("Loading next {} results".format(n + 10))
        page = session.get(url)
        c = page.content

        if any(kw in c.decode('ISO-8859-1') for kw in ROBOT_KW):
            print("Robot checking detected, handling with selenium (if installed)")
            try:
                c = get_content_with_selenium(url)
            except Exception as e:
                print("No success. The following error was raised:")
                print(e)

        # Create parser
        soup = BeautifulSoup(c, 'html.parser', from_encoding='utf-8')

        # Get stuff
        mydivs = soup.findAll("div", {"class": "gs_or"})

        for div in mydivs:
            try:
                links.append(div.find('h3').find('a').get('href'))
            except:  # catch *all* exceptions
                links.append('Look manually at: ' + url)

            try:
                title.append(div.find('h3').find('a').text)
            except:
                title.append('Could not catch title')

            try:
                citations.append(get_citations(str(div.format_string)))
            except:
                warnings.warn("Number of citations not found for {}. Appending 0".format(title[-1]))
                citations.append(0)

            try:
                year.append(get_year(div.find('div', {'class': 'gs_a'}).text))
            except:
                warnings.warn("Year not found for {}, appending 0".format(title[-1]))
                year.append(0)

            try:
                author.append(get_author(div.find('div', {'class': 'gs_a'}).text))
            except:
                author.append("Author not found")

            try:
                publisher.append(div.find('div', {'class': 'gs_a'}).text.split("-")[-1])
            except:
                publisher.append("Publisher not found")

            try:
                venue.append(" ".join(div.find('div', {'class': 'gs_a'}).text.split("-")[-2].split(",")[:-1]))
            except:
                venue.append("Venue not fount")

            rank.append(rank[-1] + 10)

        # Delay
        sleep(0.5)
    # Create a dataset
    data = pd.DataFrame(list(zip(author, title, citations, year, publisher, venue, links)), index=rank[1:],
                        columns=['Author', 'Title', 'Citations', 'Year', 'Publisher', 'Venue', 'Source'])
    data.index.name = 'Rank'
    return data


def process_data(data: pd.DataFrame, end_year: int, sortby: str) -> pd.DataFrame:
    # Add columns with number of citations per year
    data['cit/year'] = data['Citations'] / (end_year + 1 - data['Year'])
    data['cit/year'] = data['cit/year'].round(0).astype(int)

    # Sort by the selected columns, if exists
    try:
        data_ranked = data.sort_values(by=sortby, ascending=False)
    except Exception as e:
        print('Column name to be sorted not found. Sorting by the number of citations...')
        data_ranked = data.sort_values(by='Citations', ascending=False)
        print(e)

    return data_ranked


def plot_results(rank: List[int], citations: List[int], keyword: str) -> None:
    plt.plot(rank, citations, '*')
    plt.ylabel('Number of Citations')
    plt.xlabel('Rank of the keyword on Google Scholar')
    plt.title('Keyword: ' + keyword)
    plt.show()


def save_data_to_csv(data: pd.DataFrame, path: str, keyword: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)
    fpath_csv = os.path.join(path, keyword.replace(' ', '_') + '.csv')
    fpath_csv = fpath_csv[:MAX_CSV_FNAME]
    data.to_csv(fpath_csv, encoding='utf-8')


if __name__ == '__main__':
    print("Getting command line arguments...")
    start = time.time()
    GoogleScholarConfig = get_command_line_args()
    print("Running Google Scholar spider...")
    google_scholar_spider(GoogleScholarConfig=GoogleScholarConfig)
    # with tqdm(total=GoogleScholarConfig.nresults) as pbar:
    #     google_scholar_spider(GoogleScholarConfig=GoogleScholarConfig, pbar=pbar)

    end = time.time()
    print("Finished running Google Scholar spider!")
    print(f"Time taken: {end - start:.2f} seconds")
