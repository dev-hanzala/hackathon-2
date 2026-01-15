"""
Task service for business logic related to todo items.
Handles task CRUD operations with proper authorization.
"""

from typing import Optional
from uuid import UUID

from sqlmodel import Session, select

from src.db.models import Task


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
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        return session.exec(query).first()

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
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        if len(title) > 500:
            raise ValueError("Task title cannot exceed 500 characters")

        task = Task(user_id=user_id, title=title.strip(), completed=False, is_archived=False)

        session.add(task)
        session.commit()
        session.refresh(task)

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
        if not new_title or not new_title.strip():
            raise ValueError("Task title cannot be empty")

        if len(new_title) > 500:
            raise ValueError("Task title cannot exceed 500 characters")

        task = TaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            return None

        task.title = new_title.strip()
        session.add(task)
        session.commit()
        session.refresh(task)

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
        task = TaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            return None

        task.completed = True
        task.is_archived = True  # Archive when marking complete
        session.add(task)
        session.commit()
        session.refresh(task)

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
        task = TaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            return None

        task.completed = False
        task.is_archived = False  # Unarchive when marking incomplete
        session.add(task)
        session.commit()
        session.refresh(task)

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
        task = TaskService.get_task_by_id(session, task_id, user_id)
        if not task:
            return False

        session.delete(task)
        session.commit()

        return True
