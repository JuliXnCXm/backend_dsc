from pydantic import BaseModel , Field
from datetime import datetime
from enum import Enum, IntEnum

class TaskStatus(str, Enum):
    SIN_EMPEZAR = "Sin Empezar"
    EMPEZADA = "Empezada"
    FINALIZADA = "Finalizada"


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: datetime = Field(default=None) 
    completed : bool = Field(default=False)
    status: TaskStatus
    category: str


class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: str
    owner_id: str

    class Config:
        orm_mode = True
