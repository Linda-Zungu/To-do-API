from datetime import datetime, UTC
from pydantic import BaseModel, ConfigDict
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
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

# Pydantic model for API validation
class Task(BaseModel):
    id: str
    title: str
    description: str | None = None
    completed: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)