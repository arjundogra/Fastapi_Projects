from database_connection import Base
from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.sql import func

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    created_on = Column(Date, default=func.now())