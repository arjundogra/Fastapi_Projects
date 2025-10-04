from pydantic import BaseModel, Field, EmailStr, SecretStr
from datetime import date

class CreateRequest(BaseModel):
    username: str = Field(example="username")
    email: EmailStr = Field(min_length=5, max_length=20, example="email@gmail.com")
    password: SecretStr = Field(min_length=5, max_length=20, example="p@ssword")


class LoginRequest(BaseModel):
    username: str = Field(example="username")
    password: SecretStr = Field(min_length=5, max_length=20, example="p@ssword")