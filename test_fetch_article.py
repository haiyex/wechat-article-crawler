import requests
from bs4 import BeautifulSoup

url = "https://weixin.sogou.com/weixin?type=2&query=唐书房&ie=utf8&page=1"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

print("Getting article list from Sogou...")

r = requests.get(url, headers=headers, timeout=10)
r.encoding = "utf-8"

soup = BeautifulSoup(r.text, "lxml")
news_box = soup.find("div", class_="news-box")

if news_box:
    h3 = news_box.find("h3")
    if h3:
        a_tag = h3.find("a")
        if a_tag:
            article_link = a_tag.get("href", "")
            article_title = a_tag.get_text(strip=True)

            print(f"\nFound article:")
            print(f"  Title: {article_title}")
            print(f"  Sogou link: {article_link}\n")

            if article_link.startswith("/link?"):
                full_link = "https://weixin.sogou.com" + article_link
                print(f"Following redirect link: {full_link}\n")

                response = requests.get(
                    full_link, headers=headers, timeout=10, allow_redirects=False
                )

                if response.status_code in [301, 302, 303, 307, 308]:
                    redirect_url = response.headers.get("Location", "")
                    print(f"Redirected to: {redirect_url}\n")

                    if redirect_url:
                        print("Fetching article content...")
                        article_response = requests.get(
                            redirect_url, headers=headers, timeout=10
                        )
                        article_response.encoding = "utf-8"

                        print(f"Article status: {article_response.status_code}")
                        print(f"Article content length: {len(article_response.text)}")

                        article_soup = BeautifulSoup(article_response.text, "lxml")
                        article_title_elem = article_soup.find(
                            "meta", property="og:title"
                        )
                        article_desc_elem = article_soup.find(
                            "meta", property="og:description"
                        )

                        if article_title_elem:
                            print(
                                f"Meta title: {article_title_elem.get('content', '')}"
                            )
                        if article_desc_elem:
                            print(
                                f"Meta description: {article_desc_elem.get('content', '')[:100]}..."
                            )

                        content_div = article_soup.find(
                            "div", class_="rich_media_content"
                        )
                        if content_div:
                            text_content = content_div.get_text(strip=True)[:300]
                            print(f"\nContent preview: {text_content}...")
                        else:
                            print("\nContent div not found")
                else:
                    print(f"Status: {response.status_code}")
                    print(f"Response preview: {response.text[:500]}")
else:
    print("No articles found")
