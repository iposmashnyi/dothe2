from fastapi import APIRouter, HTTPException, Path
from typing import List, Optional, Dict
from datetime import datetime
import uuid

from app.db.mock_data import quadrants_db, tasks_db
from app.schema.tasks import Task, TaskCreate, TaskUpdate


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}}
)

# Helper functions
def dict_to_task(task_dict: Dict) -> Task:
    return Task(**task_dict)


# Task API Endpoints
@router.post("/", response_model=Task, status_code=201)
async def create_task(task: TaskCreate):
    """Create a new task."""
    # Validate quadrant_id exists
    if task.quadrant_id not in quadrants_db:
        raise HTTPException(status_code=400, detail="Invalid quadrant ID")

    task_id = str(uuid.uuid4())
    now = datetime.now()

    task_dict = task.model_dump()
    task_dict.update({
        "id": task_id,
        "created_at": now,
        "updated_at": now
    })

    tasks_db[task_id] = task_dict
    return dict_to_task(task_dict)


@router.get("/", response_model=List[Task])
async def read_tasks(quadrant_id: Optional[str] = None, completed: Optional[bool] = None):
    """Get all tasks with optional filtering."""
    filtered_tasks = tasks_db.values()

    if quadrant_id:
        if quadrant_id not in quadrants_db:
            raise HTTPException(status_code=400, detail="Invalid quadrant ID")
        filtered_tasks = [t for t in filtered_tasks if t["quadrant_id"] == quadrant_id]

    if completed is not None:
        filtered_tasks = [t for t in filtered_tasks if t["completed"] == completed]

    return [dict_to_task(task) for task in filtered_tasks]


@router.get("/{task_id}", response_model=Task)
async def read_task(task_id: str = Path(..., description="The ID of the task to retrieve")):
    """Get a specific task by ID."""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")

    return dict_to_task(tasks_db[task_id])


@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_update: TaskUpdate,
    task_id: str = Path(..., description="The ID of the task to update")
):
    """Update a task's details."""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")

    # Get existing task
    task_dict = tasks_db[task_id]

    # Update only fields that are provided
    update_data = task_update.model_dump(exclude_unset=True)

    # Validate quadrant_id if it's being updated
    if "quadrant_id" in update_data and update_data["quadrant_id"] not in quadrants_db:
        raise HTTPException(status_code=400, detail="Invalid quadrant ID")

    for key, value in update_data.items():
        task_dict[key] = value

    # Update the updated_at timestamp
    task_dict["updated_at"] = datetime.now()

    # Save back to DB
    tasks_db[task_id] = task_dict

    return dict_to_task(task_dict)


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: str = Path(..., description="The ID of the task to delete")):
    """Delete a task."""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")

    del tasks_db[task_id]
    return None
