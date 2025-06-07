from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


async def get_tasks(
    db: AsyncSession, quadrant_id: int | None = None, completed: bool | None = None, include_deleted: bool = False
) -> list[Task]:
    """Get tasks with optional filtering."""
    stmt = select(Task)

    if not include_deleted:
        stmt = stmt.where(~Task.is_deleted)

    if quadrant_id:
        stmt = stmt.where(Task.quadrant_id == quadrant_id)

    if completed is not None:
        stmt = stmt.where(Task.completed == completed)

    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_task_by_id(db: AsyncSession, task_id: int) -> Task | None:
    """Get a specific task by ID."""
    stmt = select(Task).where(Task.id == task_id, ~Task.is_deleted)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_task(db: AsyncSession, task: TaskCreate) -> Task:
    """Create a new task."""
    db_task = Task(
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        quadrant_id=int(task.quadrant_id),
        completed=task.completed,
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def update_task(db: AsyncSession, task_id: int, task_update: TaskUpdate) -> Task | None:
    """Update a task's details."""
    db_task = await get_task_by_id(db, task_id)
    if not db_task:
        return None

    # Update with new values
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "quadrant_id" and value:
            setattr(db_task, key, int(value))
        else:
            setattr(db_task, key, value)

    db_task.updated_at = datetime.now(UTC)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def update_task_quadrant(db: AsyncSession, task_id: int, quadrant_id: int) -> Task | None:
    """Move a task to a different quadrant."""
    db_task = await get_task_by_id(db, task_id)
    if not db_task:
        return None

    db_task.quadrant_id = quadrant_id
    db_task.updated_at = datetime.now(UTC)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def toggle_task_completion(db: AsyncSession, task_id: int, completed: bool) -> Task | None:
    """Mark a task as complete or incomplete."""
    db_task = await get_task_by_id(db, task_id)
    if not db_task:
        return None

    db_task.completed = completed
    db_task.updated_at = datetime.now(UTC)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def delete_task(db: AsyncSession, task_id: int) -> bool:
    """Soft delete a task."""
    db_task = await get_task_by_id(db, task_id)
    if not db_task:
        return False

    db_task.is_deleted = True
    db_task.deleted_at = datetime.now(UTC)
    await db.commit()
    return True
