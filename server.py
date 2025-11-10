# # server.py

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import datetime

from crawler.crawl_amazon import crawl_batch
from cleaner.clean_data import parse_amazon_html
from optimizer.ai_optimize import optimize_listing_struct
from db.save_data import create_tables, save_raw_and_clean, update_optimized
from export.export_csv import export_to_csv
from export.export_to_autopart_template import export_to_autopart_template

app = FastAPI()

# 👇 解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CollectRequest(BaseModel):
    url: str

# 接收插件传来的url
@app.post("/collect")
async def collect_item(req: CollectRequest):
    url = req.url
    create_tables()

    result = await crawl_batch([url])
    if result[url]["error"]:
        return {"status": "error", "message": result[url]["error"]}

    html = result[url]["html"]
    cleaned = parse_amazon_html(html)
    save_raw_and_clean(url, html, cleaned)

    # 打开优化工作
    optimized = optimize_listing_struct(cleaned,url=url)
    update_optimized(url, optimized)

    return {"status": "ok", "url": url, "optimized": optimized}

    ## 关闭优化工作，只返回原始采集数据
    # return {"status": "ok", "url": url, "optimized": cleaned}

# 普通导出的接口
@app.get("/export")
def export_data(start_date: str = Query(None), end_date: str = Query(None)):
    filename = f"out/result_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    export_to_csv(filename, start_date=start_date, end_date=end_date)
    return {"status": "ok", "file": filename}


# 导出到模板接口
@app.get("/export_template")
def export_template(start_date: str = Query(None), end_date: str = Query(None)):
    output = export_to_autopart_template(start_date=start_date, end_date=end_date)
    return {"status": "ok", "file": output}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=5000)