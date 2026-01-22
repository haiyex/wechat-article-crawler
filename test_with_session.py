import requests
from bs4 import BeautifulSoup
import time

session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://www.sogou.com/",
    "Connection": "keep-alive",
}
session.headers.update(headers)

print("Testing with session cookies...")

url = "https://weixin.sogou.com/weixin?type=2&query=唐书房&ie=utf8&page=1"
r = session.get(url, timeout=10)
r.encoding = "utf-8"

print(f"Status: {r.status_code}")
print(f"Cookies: {dict(session.cookies)}\n")

soup = BeautifulSoup(r.text, "lxml")
news_box = soup.find("div", class_="news-box")

if news_box:
    print("Articles found:")
    articles = news_box.find_all("h3")
    print(f"Found {len(articles)} articles\n")

    for i, h3 in enumerate(articles[:3]):
        a_tag = h3.find("a")
        if a_tag:
            article_title = a_tag.get_text(strip=True)
            article_link = a_tag.get("href", "")

            print(f"{i + 1}. {article_title}")
            print(f"   Link: {article_link[:80]}...")

            if article_link.startswith("/link?"):
                time.sleep(2)

                full_link = "https://weixin.sogou.com" + article_link
                print(f"   Fetching: {full_link}")

                response = session.get(full_link, timeout=10, allow_redirects=False)

                if response.status_code in [301, 302]:
                    redirect_url = response.headers.get("Location", "")
                    print(f"   Redirect to: {redirect_url}")

                    if "antispider" not in redirect_url:
                        article_resp = session.get(
                            redirect_url, headers=headers, timeout=10
                        )
                        article_soup = BeautifulSoup(article_resp.text, "lxml")
                        title = article_soup.find("h1", class_="rich_media_title")
                        if title:
                            print(f"   Article title: {title.get_text(strip=True)}")
                        else:
                            print(f"   Title not found, checking meta...")
                            meta_title = article_soup.find("meta", property="og:title")
                            if meta_title:
                                print(f"   Meta title: {meta_title.get('content', '')}")

                        content = article_soup.find("div", class_="rich_media_content")
                        if content:
                            print(
                                f"   Content length: {len(content.get_text(strip=True))}"
                            )
                        break
                print()
else:
    print("No articles found")
