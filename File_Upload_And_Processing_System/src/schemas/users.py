from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime

class Role(Enum):
    admin = 'admin'
    user = 'user'

class CreateUserRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, example="John Doe")
    email: str = Field(..., example="")
    password: str = Field(..., min_length=6, example="strongpassword123")
    role: Role = Field(Role.user, example="user")

class UserResponseModel(BaseModel):
    id : int
    name: str
    email: str
    role: Role
    created_on: datetime
    class Config:
        orm_mode = True