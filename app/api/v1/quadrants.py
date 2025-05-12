from fastapi import APIRouter, HTTPException, Body, Path, Query
from typing import List, Dict
from datetime import datetime
import uuid

from app.api.v1.tasks import Task, dict_to_task
from app.core.db.mock_data import quadrants_db, tasks_db
from app.schemas.quadrant import QuadrantBase, QuadrantCreate, Quadrant

router = APIRouter(
    prefix="/quadrants",
    tags=["quadrants"],
    responses={404: {"description": "Not found"}}
)

def dict_to_quadrant(quadrant_dict: Dict) -> Quadrant:
    return Quadrant(**quadrant_dict)


@router.patch("/{task_id}/quadrant", response_model=Task)
async def update_task_quadrant(
    task_id: str = Path(..., description="The ID of the task to update"),
    quadrant_id: str = Body(..., embed=True, description="The new quadrant ID")
):
    """Move a task to a different quadrant."""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")

    if quadrant_id not in quadrants_db:
        raise HTTPException(status_code=400, detail="Invalid quadrant ID")

    task_dict = tasks_db[task_id]
    task_dict["quadrant_id"] = quadrant_id
    task_dict["updated_at"] = datetime.now()

    return dict_to_task(task_dict)

@router.patch("/{task_id}/complete", response_model=Task)
async def toggle_task_completion(
    task_id: str = Path(..., description="The ID of the task to update"),
    completed: bool = Body(..., embed=True, description="The new completion status")
):
    """Mark a task as complete or incomplete."""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")

    task_dict = tasks_db[task_id]
    task_dict["completed"] = completed
    task_dict["updated_at"] = datetime.now()

    return dict_to_task(task_dict)

# New router for quadrants (can be in a separate file)
router = APIRouter(
    prefix="/quadrants",
    tags=["quadrants"],
    responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=List[Quadrant])
async def read_quadrants(include_default: bool = Query(True, description="Include default quadrants")):
    """Get all quadrants."""
    result = quadrants_db.values()

    if not include_default:
        result = [q for q in result if not q["is_default"]]

    return [dict_to_quadrant(q) for q in result]


@router.get("/{quadrant_id}", response_model=Quadrant)
async def read_quadrant(quadrant_id: str = Path(..., description="The ID of the quadrant to retrieve")):
    """Get a specific quadrant by ID."""
    if quadrant_id not in quadrants_db:
        raise HTTPException(status_code=404, detail="Quadrant not found")

    return dict_to_quadrant(quadrants_db[quadrant_id])


@router.post("/", response_model=Quadrant, status_code=201)
async def create_quadrant(quadrant: QuadrantCreate):
    """Create a new custom quadrant."""
    quadrant_id = str(uuid.uuid4())
    now = datetime.now()

    quadrant_dict = quadrant.model_dump()
    quadrant_dict.update({
        "id": quadrant_id,
        "created_at": now,
        "is_default": False
    })

    quadrants_db[quadrant_id] = quadrant_dict
    return dict_to_quadrant(quadrant_dict)


@router.put("/{quadrant_id}", response_model=Quadrant)
async def update_quadrant(
    quadrant_update: QuadrantBase,
    quadrant_id: str = Path(..., description="The ID of the quadrant to update")
):
    """Update a quadrant's details."""
    if quadrant_id not in quadrants_db:
        raise HTTPException(status_code=404, detail="Quadrant not found")

    quadrant_dict = quadrants_db[quadrant_id]

    # Prevent modification of default quadrants
    if quadrant_dict["is_default"]:
        raise HTTPException(status_code=403, detail="Cannot modify default quadrant")

    # Update with new values
    update_data = quadrant_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        quadrant_dict[key] = value

    return dict_to_quadrant(quadrant_dict)


@router.delete("/{quadrant_id}", status_code=204)
async def delete_quadrant(quadrant_id: str = Path(..., description="The ID of the quadrant to delete")):
    """Delete a custom quadrant."""
    if quadrant_id not in quadrants_db:
        raise HTTPException(status_code=404, detail="Quadrant not found")

    quadrant_dict = quadrants_db[quadrant_id]

    # Prevent deletion of default quadrants
    if quadrant_dict["is_default"]:
        raise HTTPException(status_code=403, detail="Cannot delete default quadrant")

    # Check if any tasks are using this quadrant
    tasks_with_quadrant = [t for t in tasks_db.values() if t["quadrant_id"] == quadrant_id]
    if tasks_with_quadrant:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete quadrant that is in use by {len(tasks_with_quadrant)} tasks"
        )

    del quadrants_db[quadrant_id]
    return None
