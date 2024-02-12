
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date , Enum, DateTime
from sqlalchemy.orm import relationship , validates
from config.database import Base
from schemas.Task  import TaskStatus
from config.database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, default="Jane")
    lastname = Column(String, default="Doe")
    password = Column(String)
    role = Column(String , default="USER")
    created_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    picture_url = Column(String, default="")
    tasks = relationship("Task", back_populates="owner")
    

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True)
    title = Column(String)
    description = Column(String)
    created_at = Column(DateTime)
    completed_at = Column(Date, default=None)
    completed = Column(Boolean, default=False)
    status = Column(Enum(TaskStatus))
    category = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")
    @validates('status')
    def validate_status(self, key, value):
        if value not in [TaskStatus.EMPEZADA.value, TaskStatus.FINALIZADA.value,TaskStatus.SIN_EMPEZAR.value]:
            raise ValueError("Invalid status value")
        return value