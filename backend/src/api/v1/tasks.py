"""
Tasks API endpoints (v1).
Handles CRUD operations for user tasks.
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.db.database import get_session
from src.middleware.auth import get_current_user
from src.services.task_service import TaskService
from src.db.models import Task, User
from src.api.schemas import TaskCreate, TaskUpdate


router = APIRouter(prefix="/tasks", tags=["tasks"])


# Response models
class TaskResponse:
    """Task response schema."""

    pass  # Using Task model directly for now


@router.get("", response_model=list[Task])
async def list_tasks(
    current_user: Annotated[User, Depends(get_current_user)], session: Annotated[Session, Depends(get_session)]
):
    """
    List all active tasks for the authenticated user.

    Returns tasks that are:
    - Owned by the current user
    - Not completed (completed=false)
    - Not archived (is_archived=false)

    Tasks are ordered by created_at descending (newest first).

    **Authentication Required**: Bearer token in Authorization header.

    **Response**: Array of Task objects with:
    - id: UUID
    - user_id: UUID
    - title: string
    - completed: boolean
    - is_archived: boolean
    - created_at: datetime
    - updated_at: datetime
    """
    tasks = TaskService.list_tasks_for_user(
        session=session, user_id=current_user.id, include_completed=False, include_archived=False
    )

    return tasks


@router.get("/{task_id}", response_model=Task)
async def get_task(
    task_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
):
    """
    Get a specific task by ID.

    **Authentication Required**: Bearer token in Authorization header.
    **Authorization**: User must own the task.

    Raises:
        404: Task not found or not owned by current user
    """
    task = TaskService.get_task_by_id(session=session, task_id=task_id, user_id=current_user.id)

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return task


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
):
    """
    Create a new task for the authenticated user.

    **Authentication Required**: Bearer token in Authorization header.

    **Request Body**:
    - title: string (1-500 characters, required)

    **Response**: Created Task object with:
    - id: UUID
    - user_id: UUID
    - title: string
    - completed: boolean (default: false)
    - is_archived: boolean (default: false)
    - created_at: datetime
    - updated_at: datetime

    Raises:
        422: Invalid request body (empty/missing title, title too long)
    """
    task = TaskService.create_task(session=session, user_id=current_user.id, title=task_data.title)

    return task


@router.patch("/{task_id}/complete", response_model=Task)
async def mark_task_complete(
    task_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
):
    """
    Mark a task as complete (sets completed=true and is_archived=true).

    **Authentication Required**: Bearer token in Authorization header.
    **Authorization**: User must own the task.

    **Response**: Updated Task object with completed=true and is_archived=true.

    Raises:
        404: Task not found or not owned by current user
    """
    task = TaskService.mark_task_complete(session=session, task_id=task_id, user_id=current_user.id)

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return task


@router.patch("/{task_id}/incomplete", response_model=Task)
async def mark_task_incomplete(
    task_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
):
    """
    Mark a task as incomplete (sets completed=false and is_archived=false).

    **Authentication Required**: Bearer token in Authorization header.
    **Authorization**: User must own the task.

    **Response**: Updated Task object with completed=false and is_archived=false.

    Raises:
        404: Task not found or not owned by current user
    """
    task = TaskService.mark_task_incomplete(session=session, task_id=task_id, user_id=current_user.id)

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return task


@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
):
    """
    Update a task's title.

    **Authentication Required**: Bearer token in Authorization header.
    **Authorization**: User must own the task.

    **Request Body**:
    - title: string (1-500 characters, required)

    **Response**: Updated Task object.

    **Note**: This endpoint only updates the title. Completion status remains unchanged.

    Raises:
        404: Task not found or not owned by current user
        422: Invalid request body (empty/missing title, title too long)
    """
    task = TaskService.update_task_title(
        session=session, task_id=task_id, user_id=current_user.id, new_title=task_data.title
    )

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
):
    """
    Delete a task permanently.

    **Authentication Required**: Bearer token in Authorization header.
    **Authorization**: User must own the task.

    **Response**: 204 No Content (no response body).

    **Note**: This operation is permanent and cannot be undone.

    Raises:
        404: Task not found or not owned by current user
    """
    success = TaskService.delete_task(session=session, task_id=task_id, user_id=current_user.id)

    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return None  # 204 No Content
