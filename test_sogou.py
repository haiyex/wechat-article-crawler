#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试搜狗微信搜索API的访问情况"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def test_sogou_search():
    """测试搜狗搜索API"""
    account_name = "唐书院"
    print(f"测试搜索公众号: {account_name}")

    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    # 测试文章类型搜索
    print("\n1. 测试文章类型搜索 (type=1):")
    url = f'https://weixin.sogou.com/weixin?type=1&query={quote(account_name)}&ie=utf8&page=1'
    print(f"URL: {url}")

    try:
        response = requests.get(url, headers=headers, timeout=30)
        print(f"状态码: {response.status_code}")
        print(f"内容长度: {len(response.text)}")

        # 检查是否有验证码
        if '验证码' in response.text or 'captcha' in response.text.lower():
            print("[X] 需要验证码！")
        elif '访问过于频繁' in response.text:
            print("[X] 访问过于频繁！")
        elif '微信安全中心' in response.text:
            print("[X] 被微信安全中心拦截！")
        else:
            # 尝试解析文章列表
            soup = BeautifulSoup(response.text, 'lxml')
            article_items = soup.find_all('div', class_='news-box')
            print(f"找到 {len(article_items)} 个文章框")

            if len(article_items) > 0:
                print("[OK] 找到文章列表")
                for idx, item in enumerate(article_items[:3]):
                    title_elem = item.find('h3')
                    if title_elem:
                        a_tag = title_elem.find('a')
                        if a_tag:
                            print(f"  {idx+1}. {a_tag.get_text(strip=True)}")
            else:
                print("[X] 未找到文章列表")
                # 检查是否有JavaScript动态加载
                scripts = soup.find_all('script')
                print(f"页面中有 {len(scripts)} 个script标签")

    except Exception as e:
        print(f"❌ 请求失败: {e}")

    # 测试账号类型搜索
    print("\n2. 测试账号类型搜索 (type=2):")
    url = f'https://weixin.sogou.com/weixin?type=2&query={quote(account_name)}&ie=utf8'
    print(f"URL: {url}")

    try:
        response = requests.get(url, headers=headers, timeout=30)
        print(f"状态码: {response.status_code}")
        print(f"内容长度: {len(response.text)}")

        soup = BeautifulSoup(response.text, 'lxml')
        account_items = soup.find_all('div', class_='wx-rb')
        print(f"找到 {len(account_items)} 个账号项")

        if len(account_items) > 0:
            print("[OK] 找到账号列表")
            for idx, item in enumerate(account_items[:3]):
                account_elem = item.find('h3')
                if account_elem:
                    a_tag = account_elem.find('a')
                    if a_tag:
                        print(f"  {idx+1}. {a_tag.get_text(strip=True)}")
                        print(f"      链接: {a_tag.get('href', '')}")
        else:
            print("[X] 未找到账号列表")

    except Exception as e:
        print(f"❌ 请求失败: {e}")

    print("\n3. 测试结论:")
    print("当前搜狗微信搜索可能需要JavaScript渲染才能正常显示结果。")
    print("建议使用Selenium或Playwright等工具进行渲染，或者使用专门的微信爬虫库。")

if __name__ == '__main__':
    test_sogou_search()
