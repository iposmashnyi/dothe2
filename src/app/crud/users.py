from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id).where(~User.is_deleted))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email).where(~User.is_deleted))
    return result.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    result = await db.execute(select(User).where(User.username == username).where(~User.is_deleted))
    return result.scalars().first()


async def create_user(db: AsyncSession, user_create: UserCreate) -> User:
    user = User(**user_create.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(db: AsyncSession, user: User, user_update: UserUpdate) -> User:
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user: User) -> None:
    user.is_deleted = True
    user.deleted_at = datetime.utcnow()
    await db.commit()
