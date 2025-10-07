from pydantic import BaseModel, Field
from datetime import datetime

class User(BaseModel):
    id: int
    username: str = Field(..., example="johndoe")
    email: str = Field(..., example="")