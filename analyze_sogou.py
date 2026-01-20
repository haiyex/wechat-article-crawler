#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""详细分析搜狗微信搜索API返回的内容"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def analyze_sogou_response():
    """详细分析搜狗搜索响应"""
    account_name = "唐书院"
    print(f"分析公众号: {account_name}")

    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    # 获取文章列表
    url = f'https://weixin.sogou.com/weixin?type=1&query={quote(account_name)}&ie=utf8&page=1'
    print(f"\nURL: {url}")

    try:
        response = requests.get(url, headers=headers, timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Content length: {len(response.text)}")

        soup = BeautifulSoup(response.text, 'lxml')

        # 查找所有news-box
        news_boxes = soup.find_all('div', class_='news-box')
        print(f"\nFound {len(news_boxes)} news-box elements")

        if len(news_boxes) > 0:
            print("\nFirst news-box content:")
            print("-" * 80)
            print(news_boxes[0].prettify()[:2000])
            print("-" * 80)

            # 尝试查找标题
            print("\nLooking for h3 tags in news-box:")
            h3_tags = news_boxes[0].find_all('h3')
            print(f"Found {len(h3_tags)} h3 tags")
            for idx, h3 in enumerate(h3_tags[:3]):
                print(f"\nH3 {idx+1}:")
                print(f"  Text: {h3.get_text(strip=True)}")
                a_tag = h3.find('a')
                if a_tag:
                    print(f"  Link: {a_tag.get('href', '')}")
                    print(f"  Link text: {a_tag.get_text(strip=True)}")

            # 查找所有可能的class
            print("\nAll classes in news-box:")
            all_divs = news_boxes[0].find_all('div', recursive=False)
            for div in all_divs:
                classes = div.get('class', [])
                if classes:
                    print(f"  {classes}: {div.get_text(strip=True)[:100]}")

        else:
            print("\nNo news-box found. Looking for other elements...")
            # 查找其他可能的容器
            print("\nAll div elements with class containing 'news' or 'article':")
            for div in soup.find_all('div', class_=lambda x: x and ('news' in x or 'article' in x)):
                print(f"  Class: {div.get('class')}")
                print(f"  Content: {div.get_text(strip=True)[:100]}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    analyze_sogou_response()
