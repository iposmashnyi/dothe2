from fastapi import APIRouter, HTTPException, Path, Query

from app.api.dependencies import DatabaseDep
from app.crud import quadrants as quadrant_crud
from app.crud import tasks as task_crud
from app.schemas.task import Task, TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"], responses={404: {"description": "Not found"}})


@router.post("/", response_model=Task, status_code=201)
async def create_task(db: DatabaseDep, task: TaskCreate):
    """Create a new task."""
    # Validate quadrant_id exists
    quadrant = await quadrant_crud.get_quadrant_by_id(db, int(task.quadrant_id))
    if not quadrant:
        raise HTTPException(status_code=400, detail="Invalid quadrant ID")

    return await task_crud.create_task(db, task)


@router.get("/", response_model=list[Task])
async def read_tasks(
    db: DatabaseDep,
    quadrant_id: int | None = Query(None, description="Filter by quadrant ID"),
    completed: bool | None = Query(None, description="Filter by completion status"),
):
    """Get all tasks with optional filtering."""
    # Validate quadrant_id if provided
    if quadrant_id:
        quadrant = await quadrant_crud.get_quadrant_by_id(db, quadrant_id)
        if not quadrant:
            raise HTTPException(status_code=400, detail="Invalid quadrant ID")

    return await task_crud.get_tasks(db, quadrant_id=quadrant_id, completed=completed)


@router.get("/{task_id}", response_model=Task)
async def read_task(
    db: DatabaseDep,
    task_id: int = Path(..., description="The ID of the task to retrieve"),
):
    """Get a specific task by ID."""
    task = await task_crud.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=Task)
async def update_task(
    db: DatabaseDep,
    task_update: TaskUpdate,
    task_id: int = Path(..., description="The ID of the task to update"),
):
    """Update a task's details."""
    # Validate quadrant_id if it's being updated
    if task_update.quadrant_id:
        quadrant = await quadrant_crud.get_quadrant_by_id(db, int(task_update.quadrant_id))
        if not quadrant:
            raise HTTPException(status_code=400, detail="Invalid quadrant ID")

    task = await task_crud.update_task(db, task_id, task_update)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    db: DatabaseDep,
    task_id: int = Path(..., description="The ID of the task to delete"),
):
    """Delete a task."""
    success = await task_crud.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
