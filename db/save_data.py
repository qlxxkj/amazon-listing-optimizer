# db/save_data.py
from sqlalchemy import Table, Column, Integer, String, Text, JSON, MetaData
from sqlalchemy.orm import sessionmaker
from db.db_config import engine, metadata
import json

Session = sessionmaker(bind=engine)

listings_table = Table(
    'listings', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('asin', String(50), nullable=True),
    Column('url', String(1000)),
    Column('raw', Text),
    Column('cleaned', JSON),
    Column('optimized', JSON, nullable=True)
)

def create_tables():
    metadata.create_all(engine)

def save_raw_and_clean(url, raw_html, clean_json):
    session = Session()
    ins = listings_table.insert().values(url=url, raw=raw_html, cleaned=clean_json)
    session.execute(ins)
    session.commit()
    session.close()

def update_optimized(url, optimized_json):
    session = Session()
    stmt = listings_table.update().where(listings_table.c.url == url).values(optimized=optimized_json)
    session.execute(stmt)
    session.commit()
    session.close()