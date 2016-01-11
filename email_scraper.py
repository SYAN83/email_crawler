from bs4 import BeautifulSoup
import requests
import re


emailPattern = re.compile(r"[a-z0-9\.\-+_]+(@|[\(\[\{\s]+AT[\)\]\}\s]+)[a-z0-9\.\-+_]+\.[a-z]+", re.I)


def get_emails(soup, threshold=5):
    emails_link = soup.find_all(href=re.compile("^mailto:"))
    count_link = len(emails_link)
    emails_text = soup.find_all(text=emailPattern)
    count_text = len(emails_text)
    if count_link < threshold and count_text < threshold:
        return
    elif count_text > count_link:
        return email_from_text(emails_text)
    else:
        return email_from_link(emails_link)


def email_from_link(emails_link):
    emails = []
    for tag in emails_link:
        email = tag.get("href").split("mailto:", 1)[1].strip()
        parent_tag = tag.parent
        while len(parent_tag.find_all(href=re.compile("^mailto:"))) < 2:
            if any(map(len, list(tag.strings))) > 10 or \
                            len(filter(lambda x: len(x.strip()), list(tag.strings))) > 8:
                break
            else:
                tag = parent_tag
                parent_tag = parent_tag.parent
        else:
            emails.append((email, "|".join([txt.strip() for txt in tag.strings if txt.strip()])))
    return emails


def email_from_text(emails_text):
    emails = []
    for tag in emails_text:
        email, tag = tag, tag.parent
        parent_tag = tag.parent
        while len(parent_tag.find_all(text=emailPattern)) < 2:
            if any(map(len, list(tag.strings))) > 10 or \
                            len(filter(lambda x: len(x.strip()), list(tag.strings))) > 8:
                break
            else:
                tag = parent_tag
                parent_tag = parent_tag.parent
        else:
            emails.append((email, "|".join([txt.strip() for txt in tag.strings if txt.strip()])))
    return emails


if __name__ == "__main__":
    # url = 'https://www.ece.gatech.edu/faculty-staff-directory/A'
    # url = "http://www.physics.sc.edu/people"
    # url = "http://www.csc.ncsu.edu/directories/faculty.php"
    url = "http://www.eng.auburn.edu/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    print soup
    # for link in soup.find_all("a", href=re.compile("^[^(mailto:)]")):
    #     print link
    print get_emails(soup)
    # for content in get_emails(soup):
    #     print content
