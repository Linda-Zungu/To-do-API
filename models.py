from datetime import datetime
from pydantic import BaseModel

class Task(BaseModel):
    id: str
    title: str
    completed: bool
    created_at: datetime
    updated_at: datetime