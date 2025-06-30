from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.database import Base
from app.core.db.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class Tier(Base, TimestampMixin):
    __tablename__ = "tier"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    users: Mapped[list[User]] = relationship("User", back_populates="tier")
