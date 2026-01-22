import requests
from bs4 import BeautifulSoup

url = "https://weixin.sogou.com/weixin?type=1&query=唐书房&ie=utf8&page=1"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

print("Testing Sogou WeChat search...")
print(f"URL: {url}\n")

try:
    r = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {r.status_code}")
    print(f"Encoding: {r.encoding}")
    print(f"Content length: {len(r.text)}\n")

    r.encoding = "utf-8"

    soup = BeautifulSoup(r.text, "lxml")

    all_divs = soup.find_all("div", class_=True)
    news_divs = [d for d in all_divs if any("news" in c for c in d.get("class", []))]

    print(f"Found {len(news_divs)} divs with 'news' in class name")

    for i, div in enumerate(news_divs[:5]):
        print(f"  {i + 1}. {div.get('class')}")

    news_boxes = soup.find_all("div", class_="news-box")
    print(f"\nFound {len(news_boxes)} news-box elements")

    if news_boxes:
        first_box = news_boxes[0]
        print(f"\nFirst news-box HTML snippet:")
        print(first_box.prettify()[:1000])

        h3_tags = first_box.find_all("h3")
        print(f"\nFound {len(h3_tags)} h3 tags")
        for h3 in h3_tags[:3]:
            print(f"  - {h3.get_text(strip=True)}")

        a_tags = first_box.find_all("a")
        print(f"\nFound {len(a_tags)} a tags")
        for a in a_tags[:5]:
            href = a.get("href", "")
            text = a.get_text(strip=True)
            print(f"  - {text[:50]}... -> {href[:80]}...")

except Exception as e:
    print(f"Error: {e}")
    import traceback

    traceback.print_exc()
