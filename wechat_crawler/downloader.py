import os
import aiohttp
import asyncio
import hashlib
from typing import List, Dict
from tqdm import tqdm
from urllib.parse import urlparse


class ImageDownloader:
    def __init__(self, output_dir: str, max_workers: int = 5):
        self.output_dir = output_dir
        self.max_workers = max_workers
        os.makedirs(self.output_dir, exist_ok=True)

    def _get_extension(self, url: str) -> str:
        path = urlparse(url).path
        ext = os.path.splitext(path)[1].lower()
        if not ext or ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            return '.jpg'
        return ext

    def _generate_filename(self, url: str, prefix: str = '') -> str:
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        ext = self._get_extension(url)
        if prefix:
            return f'{prefix}_{url_hash}{ext}'
        return f'{url_hash}{ext}'

    async def _download_one(self, session: aiohttp.ClientSession, url: str, filename: str, progress_bar: tqdm) -> bool:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.read()
                    filepath = os.path.join(self.output_dir, filename)
                    with open(filepath, 'wb') as f:
                        f.write(content)
                    return True
                return False
        except Exception as e:
            return False

    async def download_image_async(self, url: str, filename: str) -> bool:
        async with aiohttp.ClientSession() as session:
            connector = aiohttp.TCPConnector(limit=self.max_workers)
            async with session:
                return await self._download_one(session, url, filename, None)

    def download_images_sync(self, images: List[Dict], article_title: str = '') -> List[Dict]:
        if not images:
            return []

        updated_images = []
        semaphore = asyncio.Semaphore(self.max_workers)

        async def bounded_download(session: aiohttp.ClientSession, url: str, index: int):
            async with semaphore:
                prefix = f'{index}' if article_title else ''
                filename = self._generate_filename(url, prefix)
                success = await self._download_one(session, url, filename, None)
                if success:
                    return {
                        'url': url,
                        'local_path': f"images/{filename}",
                        'index': index
                    }
                return None

        async def download_all():
            connector = aiohttp.TCPConnector(limit=self.max_workers)
            async with aiohttp.ClientSession(connector=connector) as session:
                tasks = [bounded_download(session, img['url'], img['index']) for img in images]
                results = await asyncio.gather(*tasks)
                return [r for r in results if r is not None]

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        results = loop.run_until_complete(download_all())

        for img in images:
            for result in results:
                if result and result['url'] == img['url']:
                    updated_images.append(result)
                    break
            else:
                updated_images.append({
                    'url': img['url'],
                    'local_path': img['url'],
                    'index': img['index']
                })

        return updated_images
