#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""查找搜狗搜索页面的API端点"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import re

def find_api_endpoints():
    """查找API端点"""
    account_name = "唐书院"
    print(f"Searching for API endpoints for: {account_name}")

    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.sogou.com/'
    }

    # 获取页面
    url = f'https://weixin.sogou.com/weixin?type=1&query={quote(account_name)}&ie=utf8&page=1'
    print(f"\nFetching: {url}")

    try:
        response = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'lxml')

        # 查找所有script标签
        scripts = soup.find_all('script')
        print(f"\nFound {len(scripts)} script tags")

        # 查找包含数据的script
        for idx, script in enumerate(scripts):
            script_content = script.string if script.string else ''
            if 'article' in script_content.lower() or 'news' in script_content.lower() or 'list' in script_content.lower():
                print(f"\nScript {idx+1} (contains article/news/list):")
                print(script_content[:500])

        # 查找可能的API URL
        print("\n\nSearching for API URLs in HTML...")
        api_patterns = [
            r'https?://[^\s"\'<>]+api[^\s"\'<>]*',
            r'https?://[^\s"\'<>]+/pc/[^\s"\'<>]*\.js',
            r'https?://[^\s"\'<>]+/weixin/[^\s"\'<>]*'
        ]

        for pattern in api_patterns:
            matches = re.findall(pattern, response.text)
            if matches:
                print(f"\nPattern: {pattern}")
                for match in set(matches[:5]):  # 只显示前5个不重复的
                    print(f"  {match}")

        # 查找变量赋值
        print("\n\nSearching for variable assignments...")
        var_patterns = [
            r'var\s+\w+\s*=\s*\[.*?\];',
            r'const\s+\w+\s*=\s*\[.*?\];',
            r'let\s+\w+\s*=\s*\[.*?\];',
            r'window\.\w+\s*=\s*\[.*?\];'
        ]

        for pattern in var_patterns:
            matches = re.findall(pattern, response.text, re.DOTALL)
            if matches:
                print(f"\nPattern: {pattern}")
                for match in matches[:3]:
                    print(f"  {match[:200]}...")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

    print("\n\nConclusion:")
    print("The search results are now loaded dynamically via JavaScript.")
    print("You need to use a browser automation tool like Selenium or Playwright")
    print("to render the page and extract the article list.")

if __name__ == '__main__':
    find_api_endpoints()
