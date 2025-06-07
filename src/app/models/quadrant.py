from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.database import Base
from app.core.db.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.task import Task


class Quadrant(Base, TimestampMixin):
    __tablename__ = "quadrant"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    color: Mapped[str | None] = mapped_column(String(7), nullable=True)  # Hex color code
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    tasks: Mapped[list[Task]] = relationship("Task", back_populates="quadrant", cascade="all, delete-orphan")
