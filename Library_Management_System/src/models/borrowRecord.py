from database_connection import Base
from sqlalchemy import Column, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import date
from typing import Optional


class BorrowRecord(Base):
    __tablename__ = "borrow_records"
    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    borrow_date = Column(Date, default=date.today)
    return_date = Column(Date, nullable=True)

    member = relationship("Members", back_populates="borrow_records")
    book = relationship("Books", back_populates="borrow_records")

class BorrowRecordRequest(BaseModel):
    member_id: int
    book_id: int
    borrow_date: date = date.today()
    return_date: Optional[date] = None