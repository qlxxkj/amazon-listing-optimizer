# scripts/run_batch.py
import asyncio
from datetime import datetime
import os
import csv
from crawler.crawl_amazon import crawl_batch
from cleaner.clean_data import parse_amazon_html
from db.save_data import create_tables, save_raw_and_clean, update_optimized
from optimizer.ai_optimize import optimize_listing_struct
from export_csv import export_to_csv


def load_urls_from_csv(path):
    rows = []
    with open(path, 'r', encoding='utf-8') as f:
        r = csv.reader(f)
        for rline in r:
            if rline:
                rows.append(rline[0].strip())
    return rows


async def run(urls, concurrency=4):
    create_tables()
    batch_results = []

    res = await crawl_batch(urls, concurrency=concurrency)
    for url, info in res.items():
        if info['error']:
            print('ERROR', url, info['error'])
            continue
        raw = info['html']
        cleaned = parse_amazon_html(raw)
        save_raw_and_clean(url, raw, cleaned)
        optimized = optimize_listing_struct(cleaned)
        update_optimized(url, optimized)
        print('Optimized:', url)

        # 收集本批次数据
        batch_results.append({
            "url": url,
            "title": cleaned.get("title"),
            "price": cleaned.get("price"),
            "optimized": optimized,
            "images": cleaned.get("images") or [],
            "category": cleaned.get("category"),
            "product_dimensions": cleaned.get("product_dimensions"),
            "item_weight": cleaned.get("item_weight"),
            "shipping": cleaned.get("shipping")
        })

    # 导出当前批次 CSV
    export_to_csv(
        batch_results,
        filename=f"out/result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )


if __name__ == '__main__':
    import sys
    csv_path = sys.argv[1] if len(sys.argv) > 1 else 'input/urls.csv'
    urls = load_urls_from_csv(csv_path)
    asyncio.run(run(urls, concurrency=int(os.getenv('CONCURRENT_CRAWLS', 4))))
