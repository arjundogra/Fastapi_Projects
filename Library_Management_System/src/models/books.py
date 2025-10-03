from database_connection import Base
from sqlalchemy import String, Integer, Column
from pydantic import BaseModel, Field

class Books(Base):
    __tablename__ = "books"

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String)
    description = Column(String)
    author = Column(String)

class BooksRequest(BaseModel):
    name: str = Field(example="User Name")
    description: str 
    author: str

class BooksResponse(BaseModel):
    id: int
    name: str
    description: str 
    author: str