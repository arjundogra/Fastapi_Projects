from pydantic import BaseModel,Field, EmailStr, SecretStr
from datetime import date
from enum import Enum


class Role(Enum):
    admin = 'admin'
    user = 'user'

class CreateRequest(BaseModel):
    name: str = Field(example="Enter Your Name", min_length=3, max_length=20)
    email: EmailStr = Field(example="email@gmail.com")
    password: SecretStr = Field(example="p@ssword")
    role: Role = Field(default=Role.user)

class ResponseModel(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_on: date
    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    email: EmailStr = Field(example="email@gmail.com")
    password: SecretStr = Field(example="p@ssword")

class LoginResponse(BaseModel):
    access_token: str
    token_type: str