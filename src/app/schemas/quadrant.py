from datetime import datetime

from pydantic import BaseModel


class QuadrantBase(BaseModel):
    name: str
    description: str | None = None
    color: str | None = None  # For color-coding in UI


class QuadrantCreate(QuadrantBase):
    pass


class Quadrant(QuadrantBase):
    id: int
    created_at: datetime
    is_default: bool = False

    class Config:
        from_attributes = True
