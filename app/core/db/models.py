import uuid
from datetime import UTC, datetime

from sqlalchemy import Boolean, Column, DateTime, text
from sqlalchemy.dialects.postgresql import UUID


class UUIDMixin:
    uuid: uuid.UUID = Column(
        UUID, primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()")
    )


class TimestampMixin:
    created_at: datetime = Column(DateTime, default=datetime.now(UTC), server_default=text("current_timestamp(0)"))
    updated_at: datetime = Column(
        DateTime, nullable=True, onupdate=datetime.now(UTC), server_default=text("current_timestamp(0)")
    )


class SoftDeleteMixin:
    deleted_at: datetime = Column(DateTime, nullable=True)
    is_deleted: bool = Column(Boolean, default=False)