from sqlalchemy import Column, Date, Integer, String
from database_connection import Base
from pydantic import BaseModel
from datetime import date

class Members(Base):
    __tablename__ = 'members'
    id = Column(Integer,autoincrement=True,primary_key=True)
    name = Column(String)
    email = Column(String)
    join_date = Column(Date)


class MemberCreateRequest(BaseModel):
    name: str
    email: str
    join_date: str

class MemberResponse(BaseModel):
    id: int
    name: str
    email: str
    join_date: date