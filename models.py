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
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(datetime.timezone.utc), onupdate=datetime.now(datetime.timezone.utc))

# Pydantic model for API validation
class Task(BaseModel):
    id: str
    title: str
    description: str | None = None
    completed: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True