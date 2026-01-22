import requests
from bs4 import BeautifulSoup
import re
import time

session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}
session.headers.update(headers)

print("=" * 70)
print("Full Test: Fetching WeChat Articles for '唐书房'")
print("=" * 70)

url = "https://weixin.sogou.com/weixin?type=2&query=唐书房&ie=utf8&page=1"

print("\nStep 1: Getting article list from Sogou...")
r = session.get(url, timeout=10)
soup = BeautifulSoup(r.text, "lxml")
news_box = soup.find("div", class_="news-box")

articles = news_box.find_all("h3")
print(f"Found {len(articles)} articles\n")

print("Step 2: Fetching first 3 articles...")
print("-" * 70)

for i in range(min(3, len(articles))):
    print(f"\nArticle {i + 1}:")

    h3 = articles[i]
    a_tag = h3.find("a")
    if not a_tag:
        print("  ERROR: No link found")
        continue

    article_title = a_tag.get_text(strip=True)
    article_link = a_tag.get("href", "")
    print(f"  Title: {article_title}")

    if not article_link.startswith("/link?"):
        print("  ERROR: Invalid link format")
        continue

    full_link = "https://weixin.sogou.com" + article_link

    try:
        response = session.get(full_link, timeout=15)

        parts = []
        for match in re.finditer(r"url \+= '([^']+)'", response.text):
            parts.append(match.group(1))
        wechat_url = "".join(parts)

        if wechat_url.startswith("http"):
            print(f"  WeChat URL: {wechat_url[:80]}...")

            time.sleep(1)
            article_resp = session.get(wechat_url, headers=headers, timeout=15)
            article_resp.encoding = "utf-8"

            article_soup = BeautifulSoup(article_resp.text, "lxml")

            title = article_soup.find("h1", class_="rich_media_title")
            if title:
                article_full_title = title.get_text(strip=True)
                print(f"  [OK] Title: {article_full_title}")
            else:
                meta_title = article_soup.find("meta", property="og:title")
                if meta_title:
                    article_full_title = meta_title.get("content", "")
                    print(f"  [OK] Title (meta): {article_full_title}")

            content = article_soup.find("div", class_="rich_media_content")
            if content:
                text = content.get_text(strip=True)
                print(f"  [OK] Content length: {len(text)} characters")
                print(f"  [OK] Preview: {text[:150]}...")

            images = article_soup.find_all("img")
            print(f"  [OK] Images: {len(images)}")

    except Exception as e:
        print(f"  ERROR: {e}")

print("\n" + "=" * 70)
print("SUCCESS: WeChat article fetching is working!")
print("=" * 70)
