"""
Task service for business logic related to todo items.
Handles task CRUD operations with proper authorization.
T150: Add comprehensive logging for task operations.
"""

import logging
from typing import Optional
from uuid import UUID

from sqlmodel import Session, select

from src.db.models import Task

logger = logging.getLogger(__name__)


class TaskService:
    """Service for managing tasks."""

    @staticmethod
    def list_tasks_for_user(
        session: Session, user_id: UUID, include_completed: bool = False, include_archived: bool = False
    ) -> list[Task]:
        """
        List all tasks for a specific user.

        Args:
            session: Database session
            user_id: User ID to fetch tasks for
            include_completed: Whether to include completed tasks (default: False)
            include_archived: Whether to include archived tasks (default: False)

        Returns:
            List of Task objects belonging to the user

        By default, returns only active (not completed, not archived) tasks.
        This matches User Story 2 requirements: view active task list.
        """
        logger.info(f"Listing tasks for user: {user_id} (completed={include_completed}, archived={include_archived})")

        query = select(Task).where(Task.user_id == user_id)

        # Filter by completion status if specified
        if not include_completed:
            query = query.where(Task.completed == False)

        # Filter by archived status if specified
        if not include_archived:
            query = query.where(Task.is_archived == False)

        # Order by created_at descending (newest first)
        query = query.order_by(Task.created_at.desc())

        results = session.exec(query).all()
        logger.info(f"✅ Retrieved {len(results)} tasks for user: {user_id}")

        return list(results)

    @staticmethod
    def get_task_by_id(session: Session, task_id: UUID, user_id: UUID) -> Optional[Task]:
        """
        Get a specific task by ID for a user.

        Args:
            session: Database session
            task_id: Task ID
            user_id: User ID (for ownership validation)

        Returns:
            Task object if found and belongs to user, None otherwise
        """
        logger.debug(f"Getting task {task_id} for user {user_id}")
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(query).first()

        if task:
            logger.debug(f"✅ Task found: {task_id}")
        else:
            logger.warning(f"Task not found or unauthorized: {task_id} for user {user_id}")

        return task

    @staticmethod
    def create_task(session: Session, user_id: UUID, title: str) -> Task:
        """
        Create a new task for a user.

        Args:
            session: Database session
            user_id: User ID who owns the task
            title: Task title

        Returns:
            Created Task object

        Raises:
            ValueError: If title is empty or invalid
        """
        logger.info(f"Creating task for user {user_id}: '{title[:50]}...'")

        if not title or not title.strip():
            logger.warning(f"Task creation failed - empty title for user {user_id}")
            raise ValueError("Task title cannot be empty")

        if len(title) > 500:
            logger.warning(f"Task creation failed - title too long ({len(title)} chars) for user {user_id}")
            raise ValueError("Task title cannot exceed 500 characters")

        task = Task(user_id=user_id, title=title.strip(), completed=False, is_archived=False)

        session.add(task)
        session.commit()
        session.refresh(task)

        logger.info(f"✅ Task created: {task.id} for user {user_id}")
        return task

    @staticmethod
    def update_task_title(session: Session, task_id: UUID, user_id: UUID, new_title: str) -> Optional[Task]:
        """
        Update a task's title.

        Args:
            session: Database session
            task_id: Task ID to update
            user_id: User ID (for ownership validation)
            new_title: New task title

        Returns:
            Updated Task object if successful, None if task not found or not owned

        Raises:
            ValueError: If title is invalid
        """
        logger.info(f"Updating task {task_id} for user {user_id}")

        if not new_title or not new_title.strip():
            logger.warning(f"Update failed - empty title for task {task_id}")
            raise ValueError("Task title cannot be empty")

        if len(new_title) > 500:
            logger.warning(f"Update failed - title too long ({len(new_title)} chars) for task {task_id}")
            raise ValueError("Task title cannot exceed 500 characters")

        task = TaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            logger.warning(f"Update failed - task not found: {task_id} for user {user_id}")
            return None

        task.title = new_title.strip()
        session.add(task)
        session.commit()
        session.refresh(task)

        logger.info(f"✅ Task updated: {task_id}")
        return task

    @staticmethod
    def mark_task_complete(session: Session, task_id: UUID, user_id: UUID) -> Optional[Task]:
        """
        Mark a task as complete and archive it.

        Args:
            session: Database session
            task_id: Task ID to mark complete
            user_id: User ID (for ownership validation)

        Returns:
            Updated Task object if successful, None if task not found or not owned

        Note: Marking complete also archives the task (soft-delete).
        """
        logger.info(f"Marking task complete: {task_id} for user {user_id}")

        task = TaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            logger.warning(f"Mark complete failed - task not found: {task_id}")
            return None

        task.completed = True
        task.is_archived = True  # Archive when marking complete
        session.add(task)
        session.commit()
        session.refresh(task)

        logger.info(f"✅ Task marked complete: {task_id}")
        return task

    @staticmethod
    def mark_task_incomplete(session: Session, task_id: UUID, user_id: UUID) -> Optional[Task]:
        """
        Mark a task as incomplete and unarchive it.

        Args:
            session: Database session
            task_id: Task ID to mark incomplete
            user_id: User ID (for ownership validation)

        Returns:
            Updated Task object if successful, None if task not found or not owned
        """
        logger.info(f"Marking task incomplete: {task_id} for user {user_id}")

        task = TaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            logger.warning(f"Mark incomplete failed - task not found: {task_id}")
            return None

        task.completed = False
        task.is_archived = False  # Unarchive when marking incomplete
        session.add(task)
        session.commit()
        session.refresh(task)

        logger.info(f"✅ Task marked incomplete: {task_id}")
        return task

    @staticmethod
    def delete_task(session: Session, task_id: UUID, user_id: UUID) -> bool:
        """
        Delete a task (hard delete).

        Args:
            session: Database session
            task_id: Task ID to delete
            user_id: User ID (for ownership validation)

        Returns:
            True if task was deleted, False if task not found or not owned
        """
        logger.info(f"Deleting task: {task_id} for user {user_id}")

        task = TaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            logger.warning(f"Delete failed - task not found: {task_id}")
            return False

        session.delete(task)
        session.commit()

        logger.info(f"✅ Task deleted: {task_id}")
        return True
