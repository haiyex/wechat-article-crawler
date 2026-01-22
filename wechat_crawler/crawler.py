import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin
import time
import random
import re
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class ArticleInfo:
    title: str
    url: str
    publish_date: str
    author: str


class WechatCrawler:
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.config.user_agent})

    def get_account_articles(
        self, account_name: str, limit: Optional[int] = None
    ) -> List[ArticleInfo]:
        articles = []
        page = 1

        while True:
            try:
                url = f"https://weixin.sogou.com/weixin?type=2&query={quote(account_name)}&ie=utf8&page={page}"
                response = self.session.get(url, timeout=self.config.timeout)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "lxml")
                article_items = soup.find_all("div", class_="news-box")

                if not article_items:
                    break

                for item in article_items:
                    title_elem = item.find("h3")
                    if not title_elem:
                        continue

                    a_tag = title_elem.find("a")
                    if not a_tag:
                        continue

                    title = a_tag.get_text(strip=True)
                    url = a_tag.get("href", "")

                    if not url:
                        continue

                    date_elem = item.find("span", class_="s2")
                    date = date_elem.get_text(strip=True) if date_elem else ""

                    author_elem = item.find("a", class_="account")
                    author = (
                        author_elem.get_text(strip=True)
                        if author_elem
                        else account_name
                    )

                    articles.append(
                        ArticleInfo(
                            title=title, url=url, publish_date=date, author=author
                        )
                    )

                    if limit and len(articles) >= limit:
                        return articles

                page += 1
                time.sleep(random.uniform(1, 3))

            except Exception as e:
                print(f"获取文章列表失败: {e}")
                break

        return articles

    def get_article_content(self, article_url: str) -> Optional[str]:
        for attempt in range(self.config.retry):
            try:
                if not article_url.startswith("http"):
                    article_url = "https://weixin.sogou.com" + article_url

                response = self.session.get(article_url, timeout=self.config.timeout)
                response.raise_for_status()

                if "微信安全中心" in response.text or "访问过于频繁" in response.text:
                    time.sleep(5)
                    continue

                if "mp.weixin.qq.com" in article_url:
                    return response.text

                parts = []
                for match in re.finditer(r"url \+= '([^']+)'", response.text):
                    parts.append(match.group(1))

                if parts:
                    wechat_url = "".join(parts)
                    if wechat_url.startswith("http"):
                        time.sleep(random.uniform(1, 2))
                        article_response = self.session.get(
                            wechat_url, timeout=self.config.timeout
                        )
                        article_response.encoding = "utf-8"

                        if "微信安全中心" not in article_response.text:
                            return article_response.text

                return None

            except Exception as e:
                print(f"获取文章内容失败 (尝试 {attempt + 1}/{self.config.retry}): {e}")
                time.sleep(2)

        return None
