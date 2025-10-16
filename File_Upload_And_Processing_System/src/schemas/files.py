from pydantic import BaseModel, Field
from datetime import datetime
from schemas.users import UserResponseModel


class File(BaseModel):
    pass

class FileResponseModel(BaseModel):
    id: int
    filename: str
    filepath: str
    status: str
    uploaded_by: int
    upload_time: datetime
    updated_time: datetime
    user: UserResponseModel

    class Config:
        orm_mode = True