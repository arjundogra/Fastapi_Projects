from database_connection import Base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    role = Column(String, default='user')
    hashed_password = Column(String)
    created_on = Column(Date,default=func.now())