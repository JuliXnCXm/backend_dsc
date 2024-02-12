from pydantic import BaseModel, Field 
from schemas.Task import Task
from datetime import datetime
import uuid

class UserBase(BaseModel):
    email: str
    password: str

class User(UserBase):
    id: str
    role: str = Field(default="USER")
    name: str = Field(default="Jane")
    lastname: str = Field(default="Doe")
    is_active: bool = Field(default=True)
    created_at : datetime
    picture_url : str = Field(default="")
    tasks: list[Task] = []

    class Config:
        orm_mode = True