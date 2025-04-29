from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from sqlalchemy import create_engine

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER= GOD-PC;"
    "DATABASE=Newsdb;"
    "Trusted_Connection=yes;"
)

params = quote_plus(connection_string)
DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
