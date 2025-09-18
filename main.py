# main.py
"""Small runner for local dev: crawls a single URL and prints cleaned + optimized result."""
import asyncio
from crawler.crawl_amazon import crawl_batch
from cleaner.clean_data import parse_amazon_html
from optimizer.ai_optimize import optimize_listing_struct
from export_csv import export_to_csv

async def main():
    # url = "https://www.amazon.com/dp/B0CXXXXXXX"
    # _, html = await crawl_listing(url)
    # clean_data = parse_amazon_html(html)
    # optimized = optimize_listing(clean_data)

    # print("=== 优化前 ===")
    # print(clean_data)
    # print("=== 优化后 ===")
    # print(optimized)
    # export_csv.export_to_csv()

if __name__ == "__main__":
    asyncio.run(main())