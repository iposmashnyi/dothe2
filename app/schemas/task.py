from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    quadrant_id: str  # Reference to quadrant by ID
    completed: bool = False


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    quadrant_id: Optional[str] = None
    completed: Optional[bool] = None


class Task(TaskBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
