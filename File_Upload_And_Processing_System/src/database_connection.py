from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv()

DB_URL = os.getenv("DB_URL", "postgresql+psycopg2://user:password@localhost/dbname")
engine = create_engine(DB_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():   
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()