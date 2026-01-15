"""Unit tests for task_service.py (T162).

Tests task service methods with mocked database calls.
Focus on business logic without database dependencies.
"""

from unittest.mock import MagicMock, Mock, patch
from uuid import uuid4

import pytest

from src.db.models import Task
from src.services.task_service import TaskService


class TestTaskServiceListTasks:
    """Unit tests for listing tasks logic."""

    def test_list_tasks_for_user_active_only(self):
        """Test listing only active tasks (not completed, not archived)."""
        # Arrange
        mock_session = Mock()
        user_id = uuid4()

        mock_query = MagicMock()
        mock_query.where.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_exec_result = Mock()
        mock_exec_result.all.return_value = [
            Task(id=uuid4(), user_id=user_id, title="Task 1", completed=False, is_archived=False),
            Task(id=uuid4(), user_id=user_id, title="Task 2", completed=False, is_archived=False),
        ]
        mock_session.exec.return_value = mock_exec_result

        with patch("src.services.task_service.select") as mock_select:
            mock_select.return_value = mock_query

            # Act
            tasks = TaskService.list_tasks_for_user(
                mock_session, user_id, include_completed=False, include_archived=False
            )

            # Assert
            assert len(tasks) == 2
            assert all(isinstance(task, Task) for task in tasks)
            mock_session.exec.assert_called_once()
            # Verify filtering was applied (where called twice for completed and archived)
            assert mock_query.where.call_count == 3  # user_id, completed=False, is_archived=False

    def test_list_tasks_include_completed(self):
        """Test listing tasks including completed ones."""
        # Arrange
        mock_session = Mock()
        user_id = uuid4()

        mock_query = MagicMock()
        mock_query.where.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_exec_result = Mock()
        mock_exec_result.all.return_value = [
            Task(id=uuid4(), user_id=user_id, title="Active", completed=False, is_archived=False),
            Task(id=uuid4(), user_id=user_id, title="Completed", completed=True, is_archived=False),
        ]
        mock_session.exec.return_value = mock_exec_result

        with patch("src.services.task_service.select") as mock_select:
            mock_select.return_value = mock_query

            # Act
            tasks = TaskService.list_tasks_for_user(
                mock_session, user_id, include_completed=True, include_archived=False
            )

            # Assert
            assert len(tasks) == 2
            # Verify only 2 where calls: user_id and is_archived (not completed filter)
            assert mock_query.where.call_count == 2

    def test_list_tasks_include_all(self):
        """Test listing all tasks regardless of status."""
        # Arrange
        mock_session = Mock()
        user_id = uuid4()

        mock_query = MagicMock()
        mock_query.where.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_exec_result = Mock()
        mock_exec_result.all.return_value = [
            Task(id=uuid4(), user_id=user_id, title="Active", completed=False, is_archived=False),
            Task(id=uuid4(), user_id=user_id, title="Completed", completed=True, is_archived=False),
            Task(id=uuid4(), user_id=user_id, title="Archived", completed=False, is_archived=True),
        ]
        mock_session.exec.return_value = mock_exec_result

        with patch("src.services.task_service.select") as mock_select:
            mock_select.return_value = mock_query

            # Act
            tasks = TaskService.list_tasks_for_user(
                mock_session, user_id, include_completed=True, include_archived=True
            )

            # Assert
            assert len(tasks) == 3
            # Verify only 1 where call: user_id (no filters)
            assert mock_query.where.call_count == 1

    def test_list_tasks_empty_result(self):
        """Test listing tasks when user has no tasks."""
        # Arrange
        mock_session = Mock()
        user_id = uuid4()

        mock_query = MagicMock()
        mock_query.where.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_exec_result = Mock()
        mock_exec_result.all.return_value = []
        mock_session.exec.return_value = mock_exec_result

        with patch("src.services.task_service.select") as mock_select:
            mock_select.return_value = mock_query

            # Act
            tasks = TaskService.list_tasks_for_user(mock_session, user_id)

            # Assert
            assert len(tasks) == 0
            assert isinstance(tasks, list)


class TestTaskServiceGetTask:
    """Unit tests for getting a specific task."""

    def test_get_task_by_id_success(self):
        """Test successfully retrieving a task by ID."""
        # Arrange
        mock_session = Mock()
        task_id = uuid4()
        user_id = uuid4()

        mock_task = Task(id=task_id, user_id=user_id, title="Test Task", completed=False)

        mock_query = MagicMock()
        mock_query.where.return_value = mock_query
        mock_exec_result = Mock()
        mock_exec_result.first.return_value = mock_task
        mock_session.exec.return_value = mock_exec_result

        with patch("src.services.task_service.select") as mock_select:
            mock_select.return_value = mock_query

            # Act
            task = TaskService.get_task_by_id(mock_session, task_id, user_id)

            # Assert
            assert task is not None
            assert task.id == task_id
            assert task.user_id == user_id
            mock_session.exec.assert_called_once()

    def test_get_task_by_id_not_found(self):
        """Test returns None when task doesn't exist."""
        # Arrange
        mock_session = Mock()
        task_id = uuid4()
        user_id = uuid4()

        mock_query = MagicMock()
        mock_query.where.return_value = mock_query
        mock_exec_result = Mock()
        mock_exec_result.first.return_value = None
        mock_session.exec.return_value = mock_exec_result

        with patch("src.services.task_service.select") as mock_select:
            mock_select.return_value = mock_query

            # Act
            task = TaskService.get_task_by_id(mock_session, task_id, user_id)

            # Assert
            assert task is None

    def test_get_task_by_id_wrong_user(self):
        """Test returns None when task belongs to different user."""
        # Arrange
        mock_session = Mock()
        task_id = uuid4()
        user_id = uuid4()
        uuid4()

        # Task belongs to other_user_id, not user_id
        mock_query = MagicMock()
        mock_query.where.return_value = mock_query
        mock_exec_result = Mock()
        mock_exec_result.first.return_value = None  # Query filters by user_id, so returns None
        mock_session.exec.return_value = mock_exec_result

        with patch("src.services.task_service.select") as mock_select:
            mock_select.return_value = mock_query

            # Act
            task = TaskService.get_task_by_id(mock_session, task_id, user_id)

            # Assert
            assert task is None


class TestTaskServiceCreateTask:
    """Unit tests for task creation logic."""

    def test_create_task_success(self):
        """Test successfully creating a task."""
        # Arrange
        mock_session = Mock()
        user_id = uuid4()
        title = "New Task"

        # Act
        task = TaskService.create_task(mock_session, user_id, title)

        # Assert
        assert task.title == title.strip()
        assert task.user_id == user_id
        assert task.completed is False
        assert task.is_archived is False
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    def test_create_task_strips_whitespace(self):
        """Test task creation trims whitespace from title."""
        # Arrange
        mock_session = Mock()
        user_id = uuid4()
        title = "  Task with spaces  "

        # Act
        task = TaskService.create_task(mock_session, user_id, title)

        # Assert
        assert task.title == "Task with spaces"

    def test_create_task_empty_title_raises_error(self):
        """Test creating task with empty title raises ValueError."""
        # Arrange
        mock_session = Mock()
        user_id = uuid4()

        # Act & Assert
        with pytest.raises(ValueError, match="cannot be empty"):
            TaskService.create_task(mock_session, user_id, "")

        with pytest.raises(ValueError, match="cannot be empty"):
            TaskService.create_task(mock_session, user_id, "   ")

        mock_session.add.assert_not_called()

    def test_create_task_title_too_long_raises_error(self):
        """Test creating task with title > 500 chars raises ValueError."""
        # Arrange
        mock_session = Mock()
        user_id = uuid4()
        long_title = "A" * 501  # 501 characters

        # Act & Assert
        with pytest.raises(ValueError, match="cannot exceed 500 characters"):
            TaskService.create_task(mock_session, user_id, long_title)

        mock_session.add.assert_not_called()

    def test_create_task_max_length_succeeds(self):
        """Test creating task with exactly 500 chars succeeds."""
        # Arrange
        mock_session = Mock()
        user_id = uuid4()
        max_title = "A" * 500  # Exactly 500 characters

        # Act
        task = TaskService.create_task(mock_session, user_id, max_title)

        # Assert
        assert len(task.title) == 500
        mock_session.add.assert_called_once()


class TestTaskServiceUpdateTask:
    """Unit tests for task update logic."""

    def test_update_task_title_success(self):
        """Test successfully updating task title."""
        # Arrange
        mock_session = Mock()
        task_id = uuid4()
        user_id = uuid4()
        old_title = "Old Title"
        new_title = "New Title"

        mock_task = Task(id=task_id, user_id=user_id, title=old_title, completed=False)

        with patch.object(TaskService, "get_task_by_id", return_value=mock_task):
            # Act
            updated_task = TaskService.update_task_title(mock_session, task_id, user_id, new_title)

            # Assert
            assert updated_task is not None
            assert updated_task.title == new_title
            mock_session.add.assert_called_once()
            mock_session.commit.assert_called_once()
            mock_session.refresh.assert_called_once()

    def test_update_task_title_strips_whitespace(self):
        """Test updating task title trims whitespace."""
        # Arrange
        mock_session = Mock()
        task_id = uuid4()
        user_id = uuid4()
        new_title = "  Updated Title  "

        mock_task = Task(id=task_id, user_id=user_id, title="Old", completed=False)

        with patch.object(TaskService, "get_task_by_id", return_value=mock_task):
            # Act
            updated_task = TaskService.update_task_title(mock_session, task_id, user_id, new_title)

            # Assert
            assert updated_task.title == "Updated Title"

    def test_update_task_title_task_not_found(self):
        """Test updating non-existent task returns None."""
        # Arrange
        mock_session = Mock()
        task_id = uuid4()
        user_id = uuid4()
        new_title = "New Title"

        with patch.object(TaskService, "get_task_by_id", return_value=None):
            # Act
            updated_task = TaskService.update_task_title(mock_session, task_id, user_id, new_title)

            # Assert
            assert updated_task is None
            mock_session.add.assert_not_called()

    def test_update_task_title_empty_raises_error(self):
        """Test updating with empty title raises ValueError."""
        # Arrange
        mock_session = Mock()
        task_id = uuid4()
        user_id = uuid4()

        # Act & Assert
        with pytest.raises(ValueError, match="cannot be empty"):
            TaskService.update_task_title(mock_session, task_id, user_id, "")

        with pytest.raises(ValueError, match="cannot be empty"):
            TaskService.update_task_title(mock_session, task_id, user_id, "   ")

    def test_update_task_title_too_long_raises_error(self):
        """Test updating with title > 500 chars raises ValueError."""
        # Arrange
        mock_session = Mock()
        task_id = uuid4()
        user_id = uuid4()
        long_title = "B" * 501

        # Act & Assert
        with pytest.raises(ValueError, match="cannot exceed 500 characters"):
            TaskService.update_task_title(mock_session, task_id, user_id, long_title)


class TestTaskServiceMarkComplete:
    """Unit tests for marking tasks complete."""

    def test_mark_task_complete_success(self):
        """Test successfully marking task as complete."""
        # Arrange
        mock_session = Mock()
        task_id = uuid4()
        user_id = uuid4()

        mock_task = Task(id=task_id, user_id=user_id, title="Task", completed=False, is_archived=False)

        with patch.object(TaskService, "get_task_by_id", return_value=mock_task):
            # Act
            completed_task = TaskService.mark_task_complete(mock_session, task_id, user_id)

            # Assert
            assert completed_task is not None
            assert completed_task.completed is True
            assert completed_task.is_archived is True  # Auto-archives when completing
            mock_session.add.assert_called_once()
            mock_session.commit.assert_called_once()

    def test_mark_task_complete_not_found(self):
        """Test marking non-existent task returns None."""
        # Arrange
        mock_session = Mock()
        task_id = uuid4()
        user_id = uuid4()

        with patch.object(TaskService, "get_task_by_id", return_value=None):
            # Act
            completed_task = TaskService.mark_task_complete(mock_session, task_id, user_id)

            # Assert
            assert completed_task is None
            mock_session.add.assert_not_called()


class TestTaskServiceMarkIncomplete:
    """Unit tests for marking tasks incomplete."""

    def test_mark_task_incomplete_success(self):
        """Test successfully marking task as incomplete."""
        # Arrange
        mock_session = Mock()
        task_id = uuid4()
        user_id = uuid4()

        mock_task = Task(id=task_id, user_id=user_id, title="Task", completed=True, is_archived=True)

        with patch.object(TaskService, "get_task_by_id", return_value=mock_task):
            # Act
            incomplete_task = TaskService.mark_task_incomplete(mock_session, task_id, user_id)

            # Assert
            assert incomplete_task is not None
            assert incomplete_task.completed is False
            assert incomplete_task.is_archived is False  # Auto-unarchives when marking incomplete
            mock_session.add.assert_called_once()
            mock_session.commit.assert_called_once()

    def test_mark_task_incomplete_not_found(self):
        """Test marking non-existent task returns None."""
        # Arrange
        mock_session = Mock()
        task_id = uuid4()
        user_id = uuid4()

        with patch.object(TaskService, "get_task_by_id", return_value=None):
            # Act
            incomplete_task = TaskService.mark_task_incomplete(mock_session, task_id, user_id)

            # Assert
            assert incomplete_task is None
            mock_session.add.assert_not_called()


class TestTaskServiceDeleteTask:
    """Unit tests for task deletion logic."""

    def test_delete_task_success(self):
        """Test successfully deleting a task."""
        # Arrange
        mock_session = Mock()
        task_id = uuid4()
        user_id = uuid4()

        mock_task = Task(id=task_id, user_id=user_id, title="To Delete", completed=False)

        with patch.object(TaskService, "get_task_by_id", return_value=mock_task):
            # Act
            result = TaskService.delete_task(mock_session, task_id, user_id)

            # Assert
            assert result is True
            mock_session.delete.assert_called_once_with(mock_task)
            mock_session.commit.assert_called_once()

    def test_delete_task_not_found(self):
        """Test deleting non-existent task returns False."""
        # Arrange
        mock_session = Mock()
        task_id = uuid4()
        user_id = uuid4()

        with patch.object(TaskService, "get_task_by_id", return_value=None):
            # Act
            result = TaskService.delete_task(mock_session, task_id, user_id)

            # Assert
            assert result is False
            mock_session.delete.assert_not_called()
            mock_session.commit.assert_not_called()
