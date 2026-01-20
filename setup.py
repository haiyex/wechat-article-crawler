from setuptools import setup, find_packages

setup(
    name='wechat_crawler',
    version='1.0.0',
    description='微信公众号文章抓取工具',
    packages=find_packages(),
    install_requires=[
        'requests>=2.31.0',
        'beautifulsoup4>=4.12.0',
        'lxml>=4.9.0',
        'click>=8.1.0',
        'tqdm>=4.65.0',
        'aiohttp>=3.8.0',
        'python-dateutil>=2.8.0',
        'markdownify>=0.11.0',
    ],
    entry_points={
        'console_scripts': [
            'wechat-crawler=wechat_crawler.cli:main',
        ],
    },
)
