from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.auth_token import AuthToken
from app.models.user import User


async def create_auth_token(
    db: AsyncSession, user_id: int, ip_address: str | None = None, user_agent: str | None = None
) -> AuthToken:
    auth_token = AuthToken(user_id=user_id, ip_address=ip_address, user_agent=user_agent)
    db.add(auth_token)
    await db.commit()
    await db.refresh(auth_token)
    return auth_token


async def get_auth_token_by_token(db: AsyncSession, token: str) -> AuthToken | None:
    result = await db.execute(
        select(AuthToken)
        .where(AuthToken.token == token)
        .where(AuthToken.used_at.is_(None))
        .where(AuthToken.expires_at > datetime.now(UTC))
    )
    return result.scalars().first()


async def get_auth_token_by_code(db: AsyncSession, email: str, code: str) -> AuthToken | None:
    result = await db.execute(
        select(AuthToken)
        .join(User)
        .where(User.email == email)
        .where(AuthToken.code == code)
        .where(AuthToken.used_at.is_(None))
        .where(AuthToken.expires_at > datetime.now(UTC))
    )
    return result.scalars().first()


async def mark_token_as_used(db: AsyncSession, token: AuthToken) -> None:
    token.used_at = datetime.now(UTC)
    await db.commit()


async def cleanup_expired_tokens(db: AsyncSession) -> int:
    result = await db.execute(select(AuthToken).where(AuthToken.expires_at < datetime.now(UTC)))
    expired_tokens = result.scalars().all()

    for token in expired_tokens:
        await db.delete(token)

    await db.commit()
    return len(expired_tokens)
