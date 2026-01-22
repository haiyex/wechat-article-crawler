import requests
from bs4 import BeautifulSoup

url = "https://weixin.sogou.com/weixin?type=1&query=唐书房&ie=utf8&page=1"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

print("Testing Sogou WeChat search...")

try:
    r = requests.get(url, headers=headers, timeout=10)
    r.encoding = "utf-8"

    with open("sogou_response.html", "w", encoding="utf-8") as f:
        f.write(r.text)

    print(f"Saved response to sogou_response.html (length: {len(r.text)})")

    soup = BeautifulSoup(r.text, "lxml")

    title = soup.title.get_text() if soup.title else "No title"
    print(f"Page title: {title}\n")

    all_scripts = soup.find_all("script")
    print(f"Found {len(all_scripts)} script tags")

    for script in all_scripts[:5]:
        content = script.get_text().strip()
        if content and len(content) < 500:
            print(f"Script: {content[:200]}...")

    all_divs = soup.find_all("div", id=True)
    print(f"\nFound {len(all_divs)} divs with id")
    for div in all_divs[:10]:
        print(f"  id={div.get('id')}, class={div.get('class')}")

    search_results = soup.find("div", id="main")
    if search_results:
        print(f"\nFound main div")
        print(f"Content snippet: {search_results.get_text()[:300]}")

except Exception as e:
    print(f"Error: {e}")
    import traceback

    traceback.print_exc()
