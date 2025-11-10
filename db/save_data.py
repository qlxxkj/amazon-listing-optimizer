# db/save_data.py
from sqlalchemy import Table, Column, Integer, String, Text, JSON, MetaData, DateTime, func,Boolean, Date, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker
from db.db_config import engine, metadata
import datetime
import json
import psycopg2

Session = sessionmaker(bind=engine)

listings_table = Table(
    'listings', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('asin', String(50), nullable=True),
    Column('url', String(1000)),
    Column('raw', Text),
    Column('cleaned', JSON),
    Column('optimized', JSON, nullable=True),
    Column('created_at', DateTime, default=datetime.datetime.utcnow)  # 新增字段
)

def create_tables():
    metadata.create_all(engine)

def save_raw_and_clean(url, raw_html, clean_json):
    session = Session()
    ins = listings_table.insert().values(
        url=url,
        raw=raw_html,
        cleaned=clean_json,
        created_at=datetime.datetime.utcnow()   # 👈 保存时写入时间
        )
    session.execute(ins)
    session.commit()
    print(f"[DB] Saved raw+clean for {url}")
    session.close()

def update_optimized(url, optimized_json):
    session = Session()
    stmt = listings_table.update().where(listings_table.c.url == url).values(optimized=optimized_json)
    session.execute(stmt)
    session.commit()
    print(f"[DB] Updated optimized for {url}")
    session.close()

# 2025-11-06判断每个站点是否每天第一次执行添加

daily_run_table = Table(
    'daily_run', metadata,
    Column('site', String(50), nullable=False),
    Column('date', Date, nullable=False),
    Column('executed', Boolean, default=False, nullable=False),
    PrimaryKeyConstraint('site', 'date')
)

def check_if_first_run(site: str, date: str) -> bool:
    session = Session()
    record = session.query(daily_run_table).filter_by(site=site, date=date).first()
    session.close()
    return record is None or not record.executed

def update_run_status(site: str, date: str):
    session = Session()
    stmt = daily_run_table.insert().values(site=site, date=date, executed=True)
    session.execute(stmt)
    session.commit()
    session.close()


def get_all_cleaned(start_date=None, end_date=None):
    """
    从数据库获取 cleaned 商品数据，支持按日期过滤。
    日期格式: 'YYYY-MM-DD'
    """
    """
    使用原始 SQL 查询的版本
    """
    session = Session()

    try:
        sql = "SELECT url, cleaned, optimized, created_at FROM listings WHERE 1=1"
        params = {}

        if start_date:
            sql += " AND DATE(created_at) >= :start_date"
            params['start_date'] = start_date
        if end_date:
            sql += " AND DATE(created_at) <= :end_date"
            params['end_date'] = end_date

        sql += " ORDER BY created_at DESC"

        from sqlalchemy import text
        result = session.execute(text(sql), params)
        rows = result.fetchall()

        # 转换为字典格式
        columns = ['url', 'cleaned', 'optimized', 'created_at']
        result_dicts = [dict(zip(columns, row)) for row in rows]

        return result_dicts

    finally:
        session.close()


def load_cleaned_data_by_date(start_date=None, end_date=None):
    """
    从数据库中加载指定日期范围内的清洗 + 优化数据，
    并整理为结构化字典，供 export_to_autopart_template 使用。
    """
    records = get_all_cleaned(start_date, end_date)
    results = []


    for r in records:
        # 修复：直接从数据库读取的 JSON 字段已经是字典，不需要 json.loads
        cleaned = r.get("cleaned") or {}
        optimized = r.get("optimized") or {}

        # 如果数据是字符串格式（兼容旧数据），则尝试解析
        if isinstance(cleaned, str):
            try:
                cleaned = json.loads(cleaned) if cleaned else {}
            except Exception as e:
                print(f"[WARN] Failed to parse cleaned JSON string: {e}")
                cleaned = {}

        if isinstance(optimized, str):
            try:
                optimized = json.loads(optimized) if optimized else {}
            except Exception as e:
                print(f"[WARN] Failed to parse optimized JSON string: {e}")
                optimized = {}

        results.append({
            "url": r.get("url"),
            "asin": cleaned.get("asin", ""),
            "title": cleaned.get("title", ""),
            "price": cleaned.get("price", ""),
            "brand": cleaned.get("brand", ""),
            "features": cleaned.get("features", []),
            "description": cleaned.get("description", ""),
            "main_image": cleaned.get("main_image", ""),
            "other_images": cleaned.get("other_images", []),
            "category": cleaned.get("category", ""),
            "product_dimensions": cleaned.get("product_dimensions", ""),
            "item_weight": cleaned.get("item_weight", ""),
            "shipping": cleaned.get("shipping", ""),
            "variants": cleaned.get("variants", []),
            "optimized": optimized,
            "created_at": r.get("created_at"),
        })
    return results
