from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class QuadrantBase(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = None  # For color-coding in UI

class QuadrantCreate(QuadrantBase):
    pass

class Quadrant(QuadrantBase):
    id: str
    created_at: datetime
    is_default: bool = False

    class Config:
        from_attributes = True
