from __future__ import annotations

import secrets
import string
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.database import Base

if TYPE_CHECKING:
    from app.models.user import User


def generate_token() -> str:
    return secrets.token_urlsafe(32)


def generate_otp() -> str:
    return "".join(secrets.choice(string.digits) for _ in range(6))


class AuthToken(Base):
    __tablename__ = "auth_token"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), index=True)
    token: Mapped[str] = mapped_column(String, unique=True, index=True, default=generate_token)
    code: Mapped[str] = mapped_column(String(6), default=generate_otp)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC) + timedelta(minutes=15)
    )
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(200), nullable=True)

    user: Mapped[User] = relationship("User", back_populates="auth_tokens")
