from fastapi import APIRouter

from .quadrants import router as quadrants_router
from .tasks import router as tasks_router

router = APIRouter(prefix="/v1")
router.include_router(quadrants_router)
router.include_router(tasks_router)
