from database_connection import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Files(Base):
    __tablename__ = 'files'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filepath = Column(String,nullable= False)
    status = Column(String, default='pending')  # e.g., 'pending', 'processing', 'completed', 'failed'
    result = Column(String, nullable=True)  # To store processing results or output file path
    uploaded_by = Column(Integer, ForeignKey('users.id'))
    upload_time = Column(Date, default=func.now())
    updated_time = Column(Date, default=func.now(), onupdate=func.now())

    user = relationship('Users', back_populates='files')