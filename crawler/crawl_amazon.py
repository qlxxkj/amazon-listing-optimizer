# crawler/crawl_amazon.py
import requests
import asyncio
import os
from crawl4ai import AsyncWebCrawler
from crawler.proxy_config import get_proxy
import random


async def crawl_url(url, proxy=None, include_images=True, wait_for=None):

    proxy = proxy or get_proxy()

    # headers={
    #     "accept-language": "en-US,en;q=0.9,ja;q=0.8",
    #     "sec-ch-ua-platform": '"Windows"',
    #     },

    # user_agent=(
    #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    #     "AppleWebKit/537.36 (KHTML, like Gecko) "
    #     "Chrome/122.0.0.0 Safari/537.36"
    #     ),

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,ja;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        "sec-ch-ua-platform": '"Windows"',
    }
    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        )

    async with AsyncWebCrawler() as crawler:
        # Crawl4AI's AsyncWebCrawler supports many options; keep them minimal here
        result = await crawler.arun(
            url=url,
            proxy=proxy,
            render_js=True,
            include_images=include_images,
            browser_args=["--disable-blink-features=AutomationControlled"],
            timeout=60,
            max_wait_time=5,
            user_agent= user_agent,
            headers= headers,
            encoding = "utf-8",
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

