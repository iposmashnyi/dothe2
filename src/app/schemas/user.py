from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=30)
    username: str = Field(..., min_length=1, max_length=20)


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=30)
    username: str | None = Field(None, min_length=1, max_length=20)
    profile_image_url: str | None = None


class UserResponse(UserBase):
    id: int
    uuid: UUID
    profile_image_url: str
    is_superuser: bool
    tier_id: int | None
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True


class UserInDB(UserResponse):
    is_deleted: bool
    deleted_at: datetime | None
