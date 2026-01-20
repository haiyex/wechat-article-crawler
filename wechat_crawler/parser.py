from bs4 import BeautifulSoup
import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from urllib.parse import urljoin
from markdownify import markdownify as md


@dataclass
class Article:
    title: str
    url: str
    publish_date: str
    author: str
    content: str
    images: List[Dict]


class ArticleParser:
    @staticmethod
    def parse_article_meta(html: str) -> Optional[Dict]:
        soup = BeautifulSoup(html, 'lxml')

        title_meta = soup.find('meta', property='og:title')
        title = title_meta.get('content', '') if title_meta else ''

        if not title:
            title_elem = soup.find('h1', class_='rich_media_title')
            title = title_elem.get_text(strip=True) if title_elem else ''

        date_meta = soup.find('meta', property='og:article:published_time')
        publish_date = date_meta.get('content', '') if date_meta else ''

        if not publish_date:
            date_elem = soup.find('em', id='post-date')
            publish_date = date_elem.get_text(strip=True) if date_elem else ''

        author_meta = soup.find('meta', property='og:article:author')
        author = author_meta.get('content', '') if author_meta else ''

        if not author:
            author_elem = soup.find('span', class_='rich_media_meta_text')
            author = author_elem.get_text(strip=True) if author_elem else ''

        return {
            'title': title,
            'publish_date': publish_date,
            'author': author
        }

    @staticmethod
    def parse_article_content(html: str) -> str:
        soup = BeautifulSoup(html, 'lxml')

        content_div = soup.find('div', class_='rich_media_content')
        if not content_div:
            return ''

        for tag in content_div.find_all(['script', 'style', 'noscript']):
            tag.decompose()

        content = md(str(content_div), heading_style="ATX")

        return content.strip()

    @staticmethod
    def extract_images(html: str, base_url: str = '') -> List[Dict]:
        soup = BeautifulSoup(html, 'lxml')
        images = []

        content_div = soup.find('div', class_='rich_media_content')
        if not content_div:
            return images

        img_tags = content_div.find_all('img')

        for idx, img in enumerate(img_tags):
            data_url = img.get('data-src')
            src = img.get('src')

            url = data_url or src

            if url:
                if base_url and not url.startswith('http'):
                    url = urljoin(base_url, url)

                if 'cdn' in url or 'mmbiz' in url:
                    images.append({
                        'url': url,
                        'index': idx
                    })

        return images

    @staticmethod
    def parse_article(article_info, html: str) -> Optional[Article]:
        meta = ArticleParser.parse_article_meta(html)
        if not meta:
            return None

        content = ArticleParser.parse_article_content(html)
        images = ArticleParser.extract_images(html)

        return Article(
            title=meta['title'] or article_info.title,
            url=article_info.url,
            publish_date=meta['publish_date'] or article_info.publish_date,
            author=meta['author'] or article_info.author,
            content=content,
            images=images
        )
