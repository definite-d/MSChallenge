"""
DB Script

Handles the database setup alone.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData

DB_URL = "mysql+pymysql://root@localhost:3306/data"

Base = declarative_base()
db_engine = create_engine(DB_URL)

meta = MetaData()
con = db_engine.connect()
