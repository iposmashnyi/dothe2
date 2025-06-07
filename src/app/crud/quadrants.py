from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.quadrant import Quadrant
from app.schemas.quadrant import QuadrantBase, QuadrantCreate


async def get_quadrants(db: AsyncSession, include_default: bool = True) -> list[Quadrant]:
    """Get all quadrants."""
    stmt = select(Quadrant)
    if not include_default:
        stmt = stmt.where(~Quadrant.is_default)

    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_quadrant_by_id(db: AsyncSession, quadrant_id: int) -> Quadrant | None:
    """Get a specific quadrant by ID."""
    stmt = select(Quadrant).where(Quadrant.id == quadrant_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_quadrant(db: AsyncSession, quadrant: QuadrantCreate) -> Quadrant:
    """Create a new custom quadrant."""
    db_quadrant = Quadrant(
        name=quadrant.name,
        description=quadrant.description,
        color=quadrant.color,
        is_default=False,
    )
    db.add(db_quadrant)
    await db.commit()
    await db.refresh(db_quadrant)
    return db_quadrant


async def update_quadrant(db: AsyncSession, quadrant_id: int, quadrant_update: QuadrantBase) -> Quadrant | None:
    """Update a quadrant's details."""
    db_quadrant = await get_quadrant_by_id(db, quadrant_id)
    if not db_quadrant:
        return None

    # Prevent modification of default quadrants
    if db_quadrant.is_default:
        raise ValueError("Cannot modify default quadrant")

    # Update with new values
    update_data = quadrant_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_quadrant, key, value)

    db_quadrant.updated_at = datetime.now(UTC)
    await db.commit()
    await db.refresh(db_quadrant)
    return db_quadrant


async def delete_quadrant(db: AsyncSession, quadrant_id: int) -> bool:
    """Delete a custom quadrant."""
    db_quadrant = await get_quadrant_by_id(db, quadrant_id)
    if not db_quadrant:
        return False

    # Prevent deletion of default quadrants
    if db_quadrant.is_default:
        raise ValueError("Cannot delete default quadrant")

    # Check if any tasks are using this quadrant
    from app.models.task import Task

    stmt = select(Task).where(Task.quadrant_id == quadrant_id, ~Task.is_deleted)
    result = await db.execute(stmt)
    tasks_with_quadrant = result.scalars().all()

    if tasks_with_quadrant:
        raise ValueError(f"Cannot delete quadrant that is in use by {len(tasks_with_quadrant)} tasks")

    await db.delete(db_quadrant)
    await db.commit()
    return True
