import os
import re
from typing import Dict
from datetime import datetime
from pathlib import Path
from .parser import Article


class ArticleStorage:
    def __init__(self, base_dir: str, account_name: str):
        self.base_dir = Path(base_dir)
        self.account_name = self._sanitize_filename(account_name)
        self.account_dir = self.base_dir / self.account_name
        self.account_dir.mkdir(parents=True, exist_ok=True)

        self.image_dir = self.account_dir / 'images'
        self.image_dir.mkdir(exist_ok=True)

    def _sanitize_filename(self, filename: str) -> str:
        invalid_chars = r'[<>:"/\\|?*]'
        return re.sub(invalid_chars, '_', filename)

    def _parse_date(self, date_str: str) -> str:
        date_formats = [
            '%Y-%m-%d',
            '%Y-%m-%dT%H:%M:%S',
            '%Y年%m月%d日',
            '%Y-%m-%d %H:%M:%S',
        ]

        for fmt in date_formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue

        return '2024-01-01'

    def _generate_markdown(self, article: Article) -> str:
        date = self._parse_date(article.publish_date)

        md_content = f"""# {article.title}

**原始链接**: {article.url}
**发布日期**: {article.publish_date}
**作者**: {article.author}

---

{article.content}

---

*文章自动抓取于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return md_content

    def _generate_filename(self, article: Article) -> str:
        date = self._parse_date(article.publish_date)
        safe_title = self._sanitize_filename(article.title)
        safe_title = safe_title[:100]
        return f"{date}-{safe_title}.md"

    def save_article(self, article: Article) -> str:
        content = self._generate_markdown(article)
        filename = self._generate_filename(article)
        filepath = self.account_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(filepath)

    def get_image_dir(self) -> str:
        return str(self.image_dir)

    def get_account_dir(self) -> str:
        return str(self.account_dir)
