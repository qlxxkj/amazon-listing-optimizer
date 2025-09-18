# crawler/crawl_amazon.py
import asyncio
import os
from crawl4ai import AsyncWebCrawler
from crawler.proxy_config import get_proxy

async def crawl_url(url, proxy=None, include_images=True, wait_for=None):
    proxy = proxy or get_proxy()
    async with AsyncWebCrawler() as crawler:
        # Crawl4AI's AsyncWebCrawler supports many options; keep them minimal here
        result = await crawler.arun(
            url=url,
            proxy=proxy,
            include_images=include_images,
            browser_args=["--disable-blink-features=AutomationControlled"],
            timeout=60,
            max_wait_time=5
        )
        # result has `.html`, `.markdown`, `.json` depending on crawl4ai version
        return result.html if hasattr(result, 'html') else result.content

async def crawl_batch(urls, concurrency=4):
    sem = asyncio.Semaphore(concurrency)
    results = {}

    async def _worker(u):
        async with sem:
            try:
                html = await crawl_url(u)
                results[u] = {'html': html, 'error': None}
            except Exception as e:
                results[u] = {'html': None, 'error': str(e)}
    await asyncio.gather(*[_worker(u) for u in urls])
    return results

if __name__ == '__main__':
    sample = ['https://www.amazon.com/dp/B09XXXXXXX']
    r = asyncio.run(crawl_batch(sample))
    print(r)