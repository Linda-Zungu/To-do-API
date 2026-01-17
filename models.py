from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import Column, String, Boolean, DateTime
import uuid
from database import Base

# SQLAlchemy model for database
class TaskDB(Base):
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Pydantic model for API validation
class Task(BaseModel):
    id: str
    title: str
    completed: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True