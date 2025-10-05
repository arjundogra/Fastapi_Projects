from database_connection import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Tasks(Base):
    __tablename__ = 'tasks'

    id = Column(Integer,autoincrement=True,primary_key=True)
    title = Column(String)
    description = Column(String)
    status = Column(String, default='not started')  # e.g., 'not started', 'in progress', 'completed'
    due_date = Column(Date)
    created_on = Column(Date, default=func.now())
    updated_on = Column(Date, default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.id'))
    assigned_to = Column(Integer, ForeignKey('users.id'), nullable=True)

    creator = relationship("Users", back_populates="created_tasks", foreign_keys=[created_by])
    assignee = relationship("Users", back_populates="assigned_tasks", foreign_keys=[assigned_to])