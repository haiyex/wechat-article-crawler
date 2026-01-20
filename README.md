# 微信公众号文章抓取工具

一个基于Python的命令行工具，用于从指定微信公众号获取所有历史文章，并将文章内容保存为Markdown格式文件。

## 功能特性

- 自动获取微信公众号所有历史文章
- 提取文章完整信息（标题、链接、发布日期、作者）
- 提取文章正文内容并转换为Markdown格式
- 自动下载文章中的图片
- 支持并发下载，提高效率
- 显示抓取进度

## 安装

### 1. 克隆或下载项目

```bash
cd e:\git\z_ai
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv venv
```

### 3. 激活虚拟环境

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

```bash
python -m wechat_crawler.cli "公众号名称"
```

### 指定输出目录

```bash
python -m wechat_crawler.cli "公众号名称" -o ./output
```

### 限制文章数量

```bash
python -m wechat_crawler.cli "公众号名称" --limit 10
```

### 指定并发线程数

```bash
python -m wechat_crawler.cli "公众号名称" --workers 3
```

### 完整示例

```bash
python -m wechat_crawler.cli "机器之心" -o ./articles -l 20 -w 5
```

## 参数说明

- `account_name`: 公众号名称（必填）
- `-o, --output`: 输出目录（默认：./output）
- `-l, --limit`: 文章数量限制（可选）
- `-w, --workers`: 并发下载线程数（默认：5）

## 输出结构

```
output/
├── 公众号名称/
│   ├── 2024-01-15-文章标题1.md
│   ├── 2024-01-14-文章标题2.md
│   └── images/
│       ├── img1.jpg
│       ├── img2.jpg
│       └── img3.jpg
```

## Markdown文件格式

每个文章生成的Markdown文件包含：

```markdown
# 文章标题

**原始链接**: [文章链接]
**发布日期**: [日期]
**作者**: [作者]

---

[文章正文内容]

---

*文章自动抓取于 [抓取时间]*
```

## 注意事项

1. **反爬虫机制**: 微信公众号有反爬虫机制，建议：
   - 不要频繁抓取
   - 适当控制并发数
   - 抓取失败时等待一段时间再重试

2. **访问限制**: 部分公众号可能设置了访问限制，导致无法获取文章

3. **搜狗搜索API**: 本工具使用搜狗搜索API获取文章列表，API可能会有访问频率限制

4. **版权声明**: 本工具仅用于个人学习和研究，请尊重原创者版权

## 依赖项

- requests: HTTP请求库
- beautifulsoup4: HTML解析库
- lxml: BeautifulSoup解析器
- click: 命令行参数解析
- tqdm: 进度条显示
- aiohttp: 异步HTTP客户端
- python-dateutil: 日期处理
- markdownify: HTML转Markdown

## 常见问题

### Q: 为什么有些文章抓取失败？

A: 可能的原因：
- 文章已被删除或设置为不可见
- 访问过于频繁被限制
- 网络连接问题

### Q: 如何提高抓取速度？

A: 可以适当增加并发线程数：
```bash
python -m wechat_crawler.cli "公众号名称" --workers 10
```
但不建议设置过高，以免被限制访问。

### Q: 图片下载失败怎么办？

A: 失败的图片会保留原始URL链接，不会影响文章内容的保存。

## 开发说明

项目结构：
```
z_ai/
├── wechat_crawler/          # 主程序目录
│   ├── __init__.py
│   ├── __main__.py
│   ├── crawler.py          # 爬虫模块
│   ├── parser.py           # 解析模块
│   ├── downloader.py       # 下载模块
│   ├── storage.py          # 存储模块
│   └── cli.py              # 命令行入口
├── config.py                # 配置文件
├── requirements.txt         # 依赖包
└── README.md               # 使用说明
```

## 许可证

MIT License
