from __future__ import annotations

import uuid as uuid_pkg
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.database import Base
from app.core.db.mixins import SoftDeleteMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.tier import Tier


class User(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(30))
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)

    profile_image_url: Mapped[str] = mapped_column(String, default="")
    uuid: Mapped[uuid_pkg.UUID] = mapped_column(default=uuid_pkg.uuid4, unique=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    tier_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("tier.id"), index=True, default=None)

    tier: Mapped[Tier | None] = relationship("Tier", back_populates="users")
