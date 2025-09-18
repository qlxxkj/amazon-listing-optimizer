# db/db_config.py
import os
from sqlalchemy import create_engine, MetaData

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise RuntimeError('DATABASE_URL not set in environment')

engine = create_engine(DATABASE_URL, echo=False, future=True)
metadata = MetaData()

# Ensure you create tables manually or use migrations (Alembic)