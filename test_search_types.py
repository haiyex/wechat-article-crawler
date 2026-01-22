import requests
from bs4 import BeautifulSoup


def test_search(account_name, search_type):
    if search_type == 1:
        type_name = "account (公众号)"
    else:
        type_name = "article (文章)"

    url = f"https://weixin.sogou.com/weixin?type={search_type}&query={account_name}&ie=utf8&page=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    print(f"\nTesting {type_name} search...")
    print(f"URL: {url}\n")

    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.encoding = "utf-8"

        soup = BeautifulSoup(r.text, "lxml")
        title = soup.title.get_text() if soup.title else "No title"

        print(f"Status: {r.status_code}")
        print(f"Title: {title}\n")

        news_boxes = soup.find_all("div", class_="news-box")
        print(f"Found {len(news_boxes)} news-box elements")

        if news_boxes:
            for i, box in enumerate(news_boxes[:3]):
                print(f"\nResult {i + 1}:")
                h3 = box.find("h3")
                if h3:
                    a_tag = h3.find("a")
                    if a_tag:
                        print(f"  Title: {a_tag.get_text(strip=True)}")
                        print(f"  URL: {a_tag.get('href', '')[:80]}...")

        no_result = soup.find("div", id="noresult_part1_container")
        if no_result:
            print(f"\nNo result message found:")
            print(f"  {no_result.get_text(strip=True)}")

    except Exception as e:
        print(f"Error: {e}")


print("Testing Sogou WeChat search for '唐书房'")
print("=" * 60)

test_search("唐书房", 1)
test_search("唐书房", 2)
test_search("投资", 2)
