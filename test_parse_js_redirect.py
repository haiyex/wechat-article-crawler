import requests
from bs4 import BeautifulSoup
import time
import re
import json

session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}
session.headers.update(headers)

url = "https://weixin.sogou.com/weixin?type=2&query=唐书房&ie=utf8&page=1"
r = session.get(url, timeout=10)
soup = BeautifulSoup(r.text, "lxml")
news_box = soup.find("div", class_="news-box")

articles = news_box.find_all("h3")
h3 = articles[0]
a_tag = h3.find("a")
article_link = a_tag.get("href", "")
full_link = "https://weixin.sogou.com" + article_link

print(f"Fetching: {full_link}")
response = session.get(full_link, timeout=15)

with open("redirect_page.html", "w", encoding="utf-8") as f:
    f.write(response.text)

print("Saved response to redirect_page.html")

url_match = re.search(r"url \+= '([^']+)'", response.text)
if url_match:
    parts = []
    for match in re.finditer(r"url \+= '([^']+)'", response.text):
        parts.append(match.group(1))
    wechat_url = "".join(parts)
    print(f"Found WeChat URL: {wechat_url}")

    if wechat_url.startswith("http"):
        print("\nFetching from WeChat...")
        article_resp = session.get(wechat_url, headers=headers, timeout=15)
        article_resp.encoding = "utf-8"

        article_soup = BeautifulSoup(article_resp.text, "lxml")

        title = article_soup.find("h1", class_="rich_media_title")
        if title:
            print(f"Title: {title.get_text(strip=True)}")
        else:
            meta_title = article_soup.find("meta", property="og:title")
            if meta_title:
                print(f"Meta title: {meta_title.get('content', '')}")

        content = article_soup.find("div", class_="rich_media_content")
        if content:
            text = content.get_text(strip=True)
            print(f"Content length: {len(text)}")
            print(f"Preview: {text[:300]}...")
