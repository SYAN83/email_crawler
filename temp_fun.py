from bs4 import BeautifulSoup
from urlparse import urlsplit
from collections import deque
import requests
import requests.exceptions
import HTMLParser
import re
import email_scraper as es
import pandas as pd


def is_html(url):
    # Check if URL is valid HTML page
    try:
        resp_head = requests.head(url)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        return False
    else:
        # print resp_head.headers["content-type"]
        if "content-type" in resp_head.headers and \
                        "text/html" in resp_head.headers["content-type"]:
            return True
        else:
            return False


def crawl(url_list, dept=None, file_path=None, threshold=5, limit=None, sameDomain=True, subPath=True):
    # urls to crawl
    processed_urls = set()
    url_queue = deque(url_list)
    # search url in queue
    while url_queue:
        if limit and len(processed_urls) > limit:
            return
        # crawled emails
        # dequeue url for search
        from_url = url_queue.popleft()
        # extract base url to resolve relative links
        from_parsed = urlsplit(from_url)
        base_url = "{0.scheme}://{0.netloc}".format(from_parsed)
        processed_urls.add(from_url)
        if not from_parsed.path:
            from_url += "/"
            from_parsed = urlsplit(from_url)
        print "Processing ---> {0}".format(from_url)
        # check if URL is HTML webpage
        if not is_html(from_url):
            continue
        # get response from url
        try:
            response = requests.get(from_url)
            soup = BeautifulSoup(response.text, "html.parser")
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            # ignore pages with errors
            continue
        except HTMLParser.HTMLParseError:
            continue
        emails = pd.DataFrame(es.get_emails(soup, threshold=threshold), columns=["Email", "Info"])
        emails.loc[:,"Link"] = pd.Series([from_url] * len(emails.index), index=emails.index)
        emails.loc[:,"Dept"] = pd.Series([dept] * len(emails.index), index=emails.index)
        if len(emails.index):
            if file_path is None:
                print emails
            else:
                emails.to_csv(file_path, index=False, header=False, mode='a', encoding="utf-8")
        # parse href link and extract clickable links for later parsing
        for link in soup.find_all("a", href=re.compile("^[^(mailto:)]")):
            to_link = link.get("href").strip().split("#", 1)[0]
            to_parsed = urlsplit(to_link)
            if not to_parsed.netloc:
                to_link = base_url + to_link
                to_parsed = urlsplit(to_link)
            if sameDomain:
                if from_parsed.netloc != to_parsed.netloc:
                    continue
            elif subPath:
                if from_parsed.path not in to_parsed.path:
                    continue

            if to_link and to_link not in url_queue and to_link not in processed_urls:
                url_queue.append(to_link)



if __name__ == "__main__":
    urls = ["http://www.regent.edu/"]
    dept = 'sc'
    crawl(urls, dept, limit=50)