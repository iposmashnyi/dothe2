from fastapi import APIRouter, Body, HTTPException, Path, Query

from app.api.dependencies import DatabaseDep
from app.crud import quadrants as quadrant_crud
from app.crud import tasks as task_crud
from app.schemas.quadrant import Quadrant, QuadrantBase, QuadrantCreate
from app.schemas.task import Task

router = APIRouter(
    prefix="/quadrants",
    tags=["Quadrants"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[Quadrant])
async def read_quadrants(
    db: DatabaseDep,
    include_default: bool = Query(True, description="Include default quadrants"),
):
    """Get all quadrants."""
    quadrants = await quadrant_crud.get_quadrants(db, include_default=include_default)
    return quadrants


@router.get("/{quadrant_id}", response_model=Quadrant)
async def read_quadrant(
    db: DatabaseDep,
    quadrant_id: int = Path(..., description="The ID of the quadrant to retrieve"),
):
    """Get a specific quadrant by ID."""
    quadrant = await quadrant_crud.get_quadrant_by_id(db, quadrant_id)
    if not quadrant:
        raise HTTPException(status_code=404, detail="Quadrant not found")
    return quadrant


@router.post("/", response_model=Quadrant, status_code=201)
async def create_quadrant(db: DatabaseDep, quadrant: QuadrantCreate):
    """Create a new custom quadrant."""
    return await quadrant_crud.create_quadrant(db, quadrant)


@router.put("/{quadrant_id}", response_model=Quadrant)
async def update_quadrant(
    db: DatabaseDep,
    quadrant_update: QuadrantBase,
    quadrant_id: int = Path(..., description="The ID of the quadrant to update"),
):
    """Update a quadrant's details."""
    try:
        quadrant = await quadrant_crud.update_quadrant(db, quadrant_id, quadrant_update)
        if not quadrant:
            raise HTTPException(status_code=404, detail="Quadrant not found")
        return quadrant
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.delete("/{quadrant_id}", status_code=204)
async def delete_quadrant(
    db: DatabaseDep,
    quadrant_id: int = Path(..., description="The ID of the quadrant to delete"),
):
    """Delete a custom quadrant."""
    try:
        success = await quadrant_crud.delete_quadrant(db, quadrant_id)
        if not success:
            raise HTTPException(status_code=404, detail="Quadrant not found")
    except ValueError as e:
        if "Cannot delete default quadrant" in str(e):
            raise HTTPException(status_code=403, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))


# Task operations related to quadrants
@router.patch("/{task_id}/quadrant", response_model=Task)
async def update_task_quadrant(
    db: DatabaseDep,
    task_id: int = Path(..., description="The ID of the task to update"),
    quadrant_id: int = Body(..., embed=True, description="The new quadrant ID"),
):
    """Move a task to a different quadrant."""
    # Validate quadrant exists
    quadrant = await quadrant_crud.get_quadrant_by_id(db, quadrant_id)
    if not quadrant:
        raise HTTPException(status_code=400, detail="Invalid quadrant ID")

    task = await task_crud.update_task_quadrant(db, task_id, quadrant_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}/complete", response_model=Task)
async def toggle_task_completion(
    db: DatabaseDep,
    task_id: int = Path(..., description="The ID of the task to update"),
    completed: bool = Body(..., embed=True, description="The new completion status"),
):
    """Mark a task as complete or incomplete."""
    task = await task_crud.toggle_task_completion(db, task_id, completed)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
