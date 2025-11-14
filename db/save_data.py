# db/save_data.py
from sqlalchemy import Table, Column, Integer, String, Text, JSON, MetaData, DateTime, func,Boolean, Date, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker
from db.db_config import engine, metadata
import datetime
import json
import psycopg2
from sqlalchemy import select, and_

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

def get_all_data(start_date=None,end_date=None):
    session = Session()

    query = select(listings_table)
    if start_date and end_date:
        query = query.where(
            and_(
                listings_table.c.created_at >= start_date,
                listings_table.c.created_at < end_date + " 23:59:59"
            )
        )
    elif start_date:
        query = query.where(listings_table.c.created_at >= start_date)
    elif end_date:
        query = query.where(listings_table.c.created_at < end_date + " 23:59:59")

    rows = session.execute(query).all()
    if not rows:
        print("[EXPORT] 没有符合条件的数据")
        return
    session.close()
    return rows
