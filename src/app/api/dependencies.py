from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.database import async_get_db
from app.core.security import verify_token
from app.crud.users import get_user_by_id
from app.models.user import User

security = HTTPBearer()


async def get_db():
    async for session in async_get_db():
        yield session


DatabaseDep = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: DatabaseDep,
) -> User:
    token = credentials.credentials
    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await get_user_by_id(db, int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.is_deleted:
        raise HTTPException(status_code=400, detail="Deleted user")
    return current_user


async def get_current_superuser(current_user: Annotated[User, Depends(get_current_active_user)]) -> User:
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return current_user


CurrentUserDep = Annotated[User, Depends(get_current_active_user)]
SuperUserDep = Annotated[User, Depends(get_current_superuser)]
