from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy.orm import declarative_base
load_dotenv()

db_url = os.getenv('DB_URL','postgresql://')

engine = create_engine(url=db_url)

session = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()