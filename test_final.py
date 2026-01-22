import requests
from bs4 import BeautifulSoup
import time
import re

session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://www.sogou.com/",
}
session.headers.update(headers)

print("=" * 70)
print("Testing WeChat article fetching for '唐书房'")
print("=" * 70)

url = "https://weixin.sogou.com/weixin?type=2&query=唐书房&ie=utf8&page=1"

print("\n1. Getting article list from Sogou...")
r = session.get(url, timeout=10)
r.encoding = "utf-8"

soup = BeautifulSoup(r.text, "lxml")
news_box = soup.find("div", class_="news-box")

if not news_box:
    print("   ERROR: No articles found")
    exit(1)

articles = news_box.find_all("h3")
print(f"   Found {len(articles)} articles\n")

print("2. Fetching first article...")
h3 = articles[0]
a_tag = h3.find("a")

if not a_tag:
    print("   ERROR: No link found")
    exit(1)

article_title = a_tag.get_text(strip=True)
article_link = a_tag.get("href", "")

print(f"   Title: {article_title}")
print(f"   Sogou link: {article_link[:80]}...\n")

if not article_link.startswith("/link?"):
    print("   ERROR: Not a redirect link")
    exit(1)

full_link = "https://weixin.sogou.com" + article_link
print(f"3. Following redirect...")

try:
    response = session.get(full_link, timeout=15, allow_redirects=False)
    print(f"   Status: {response.status_code}")

    if response.status_code not in [301, 302, 303, 307, 308]:
        print(f"   WARNING: Expected redirect, got {response.status_code}")
        print(f"   Response preview: {response.text[:500]}")
        exit(1)

    redirect_url = response.headers.get("Location", "")
    print(f"   Redirect to: {redirect_url[:100]}...\n")

    if "antispider" in redirect_url:
        print("   ERROR: Blocked by anti-spider")
        print("   This means Sogou requires browser cookies or verification")
        exit(1)

    if redirect_url.startswith("http"):
        print("4. Fetching actual article from WeChat...")
        time.sleep(1)

        article_resp = session.get(redirect_url, headers=headers, timeout=15)
        article_resp.encoding = "utf-8"

        print(f"   Status: {article_resp.status_code}")
        print(f"   Content length: {len(article_resp.text)}\n")

        article_soup = BeautifulSoup(article_resp.text, "lxml")

        title = article_soup.find("h1", class_="rich_media_title")
        if title:
            print("5. Article found successfully!")
            print(f"   Title: {title.get_text(strip=True)}")
        else:
            print("5. Checking meta title...")
            meta_title = article_soup.find("meta", property="og:title")
            if meta_title:
                print(f"   Meta title: {meta_title.get('content', '')}")

        content = article_soup.find("div", class_="rich_media_content")
        if content:
            text_len = len(content.get_text(strip=True))
            print(f"   Content: {text_len} characters")
            preview = content.get_text(strip=True)[:200]
            print(f"   Preview: {preview}...")

        images = article_soup.find_all("img")
        print(f"   Images: {len(images)}")

        print("\n" + "=" * 70)
        print("SUCCESS: Can fetch WeChat articles via Sogou")
        print("=" * 70)

    else:
        print(f"   ERROR: Invalid redirect URL: {redirect_url}")

except Exception as e:
    print(f"   ERROR: {e}")
    import traceback

    traceback.print_exc()
