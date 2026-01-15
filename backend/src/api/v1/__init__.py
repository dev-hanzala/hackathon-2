"""API v1 router setup."""

from fastapi import APIRouter

from .auth import router as auth_router
from .tasks import router as tasks_router

router = APIRouter(prefix="/api/v1", tags=["v1"])

# Include auth router
router.include_router(auth_router)

# Include tasks router (User Story 2)
router.include_router(tasks_router)

__all__ = ["router"]
