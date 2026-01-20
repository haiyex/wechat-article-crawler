import click
from tqdm import tqdm
from .crawler import WechatCrawler
from .parser import ArticleParser
from .downloader import ImageDownloader
from .storage import ArticleStorage
import sys


@click.command()
@click.argument('account_name')
@click.option('--output', '-o', default='./output', help='输出目录')
@click.option('--limit', '-l', default=None, type=int, help='文章数量限制')
@click.option('--workers', '-w', default=5, type=int, help='并发下载线程数')
def main(account_name, output, limit, workers):
    """
    微信公众号文章抓取工具

    示例:
        python -m wechat_crawler.cli "公众号名称" -o ./output
        python -m wechat_crawler.cli "公众号名称" --limit 10
    """
    click.echo(f'开始抓取公众号: {account_name}')

    try:
        from config import config

        crawler = WechatCrawler(config)

        click.echo('正在获取文章列表...')
        articles_info = crawler.get_account_articles(account_name, limit)

        if not articles_info:
            click.echo('未找到该公众号的文章，请确认公众号名称是否正确')
            sys.exit(1)

        click.echo(f'共找到 {len(articles_info)} 篇文章')

        storage = ArticleStorage(output, account_name)
        image_downloader = ImageDownloader(storage.get_image_dir(), workers)

        success_count = 0
        fail_count = 0

        with tqdm(total=len(articles_info), desc='抓取进度') as pbar:
            for idx, article_info in enumerate(articles_info, 1):
                try:
                    pbar.set_description(f'正在处理 {idx}/{len(articles_info)}: {article_info.title[:20]}')

                    html = crawler.get_article_content(article_info.url)
                    if not html:
                        fail_count += 1
                        pbar.write(f'获取内容失败: {article_info.title}')
                        continue

                    article = ArticleParser.parse_article(article_info, html)
                    if not article:
                        fail_count += 1
                        pbar.write(f'解析失败: {article_info.title}')
                        continue

                    if article.images:
                        article.images = image_downloader.download_images_sync(article.images, article.title)

                    filepath = storage.save_article(article)
                    success_count += 1

                except Exception as e:
                    fail_count += 1
                    pbar.write(f'处理失败: {article_info.title} - {str(e)}')

                pbar.update(1)

        click.echo(f'\n抓取完成！')
        click.echo(f'成功: {success_count} 篇')
        click.echo(f'失败: {fail_count} 篇')
        click.echo(f'输出目录: {storage.get_account_dir()}')

    except KeyboardInterrupt:
        click.echo('\n用户中断')
        sys.exit(1)
    except Exception as e:
        click.echo(f'发生错误: {str(e)}', err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
