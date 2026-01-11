"""API v1 router setup."""

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["v1"])

# Import routers for different endpoints
# These will be populated as we implement user stories
# from .auth import router as auth_router
# from .tasks import router as tasks_router

# Include routers
# router.include_router(auth_router)
# router.include_router(tasks_router)

__all__ = ["router"]
