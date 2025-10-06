from pydantic import BaseModel, Field
from datetime import date, timedelta
from typing import Optional
from enum import Enum

class CreateTaskRequest(BaseModel):
    title: str = Field(example="Task Title", min_length=3, max_length=50)
    description: str = Field(example="Task Description", min_length=10, max_length=300)
    due_date: date = Field(example=date.today() + timedelta(days=7))  # Default due date is one week from today
    assigned_to: Optional[int] = Field(None, example=2)  # User ID of the assignee
    status: Optional[str] = Field('not started', example="not started")  # Default status
    class Config:
        orm_mode = True

class UpdateTaskRequest(BaseModel):
    title: Optional[str] = Field(None, example="Updated Task Title", min_length=3, max_length=50)
    description: Optional[str] = Field(None, example="Updated Task Description", min_length=10, max_length=300)
    due_date: Optional[date] = Field(None, example="2024-01-31")
    assigned_to: Optional[int] = Field(None, example=3)  # User ID of the new assignee
    status: Optional[str] = Field(None, example="in progress")  # e.g., 'not started', 'in progress', 'completed'
    class Config:
        orm_mode = True

class TaskResponseModel(BaseModel):
    id: int
    title: str
    description: str
    status: str
    due_date: date
    created_on: date
    updated_on: date
    created_by: int
    assigned_to: Optional[int] = None
    class Config:
        orm_mode = True

