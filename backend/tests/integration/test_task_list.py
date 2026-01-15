"""
Integration tests for task list functionality (User Story 2).
Tests the complete flow of viewing tasks for authenticated users.
"""

import pytest
from httpx import AsyncClient
from sqlmodel import Session

from src.db.models import Task, User


class TestTaskListIntegration:
    """Integration tests for GET /tasks endpoint (US2)."""

    @pytest.mark.asyncio
    async def test_list_tasks_authenticated_user_with_tasks(
        self, client: AsyncClient, auth_headers: dict[str, str], db_session: Session, registered_user: User
    ):
        """T053: Test list_tasks endpoint with authenticated user and multiple tasks."""
        # Create 5 tasks for the registered user
        task_titles = ["Buy groceries", "Write code", "Exercise", "Read book", "Call mom"]

        for title in task_titles:
            task = Task(user_id=registered_user.id, title=title)
            db_session.add(task)

        db_session.commit()

        # Fetch task list
        response = await client.get("/api/v1/tasks", headers=auth_headers)

        assert response.status_code == 200
        tasks = response.json()
        assert isinstance(tasks, list)
        assert len(tasks) == 5

        # Verify task details
        returned_titles = {task["title"] for task in tasks}
        assert returned_titles == set(task_titles)

        # Verify all tasks belong to the user
        for task in tasks:
            assert task["user_id"] == str(registered_user.id)
            assert task["completed"] is False
            assert task["is_archived"] is False

    @pytest.mark.asyncio
    async def test_list_tasks_empty_for_new_user(self, client: AsyncClient, db_session: Session):
        """T054: Test empty task list for authenticated user with no tasks."""
        # Create a new user with no tasks
        from src.middleware.auth import get_password_hash

        password_hash = get_password_hash("NewUser123")
        new_user = User(email="newuser@example.com", password_hash=password_hash)
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)

        # Sign in to get token
        signin_response = await client.post(
            "/api/v1/auth/signin", json={"email": "newuser@example.com", "password": "NewUser123"}
        )
        assert signin_response.status_code == 200

        token = signin_response.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Fetch task list
        response = await client.get("/api/v1/tasks", headers=headers)

        assert response.status_code == 200
        tasks = response.json()
        assert isinstance(tasks, list)
        assert len(tasks) == 0

    @pytest.mark.asyncio
    async def test_list_tasks_requires_authentication(self, client: AsyncClient):
        """T055: Test unauthenticated request returns 401 Unauthorized."""
        response = await client.get("/api/v1/tasks")

        assert response.status_code == 401
        error = response.json()
        assert "detail" in error

    @pytest.mark.asyncio
    async def test_list_tasks_user_data_isolation(self, client: AsyncClient, db_session: Session):
        """T056: Test user A's tasks not visible to user B."""
        from src.middleware.auth import get_password_hash, create_access_token

        # Create User A with tasks
        password_hash_a = get_password_hash("UserA123")
        user_a = User(email="usera@example.com", password_hash=password_hash_a)
        db_session.add(user_a)
        db_session.commit()
        db_session.refresh(user_a)

        task_a1 = Task(user_id=user_a.id, title="User A Task 1")
        task_a2 = Task(user_id=user_a.id, title="User A Task 2")
        db_session.add(task_a1)
        db_session.add(task_a2)

        # Create User B with tasks
        password_hash_b = get_password_hash("UserB123")
        user_b = User(email="userb@example.com", password_hash=password_hash_b)
        db_session.add(user_b)
        db_session.commit()
        db_session.refresh(user_b)

        task_b1 = Task(user_id=user_b.id, title="User B Task 1")
        db_session.add(task_b1)
        db_session.commit()

        # Get User A's tasks
        token_a = create_access_token(data={"sub": str(user_a.id), "email": user_a.email})
        headers_a = {"Authorization": f"Bearer {token_a}"}

        response_a = await client.get("/api/v1/tasks", headers=headers_a)
        assert response_a.status_code == 200
        tasks_a = response_a.json()
        assert len(tasks_a) == 2
        assert all(task["user_id"] == str(user_a.id) for task in tasks_a)

        # Get User B's tasks
        token_b = create_access_token(data={"sub": str(user_b.id), "email": user_b.email})
        headers_b = {"Authorization": f"Bearer {token_b}"}

        response_b = await client.get("/api/v1/tasks", headers=headers_b)
        assert response_b.status_code == 200
        tasks_b = response_b.json()
        assert len(tasks_b) == 1
        assert all(task["user_id"] == str(user_b.id) for task in tasks_b)

        # Verify no cross-contamination
        task_a_titles = {task["title"] for task in tasks_a}
        task_b_titles = {task["title"] for task in tasks_b}
        assert "User A Task 1" in task_a_titles
        assert "User A Task 2" in task_a_titles
        assert "User B Task 1" in task_b_titles
        assert "User B Task 1" not in task_a_titles
        assert "User A Task 1" not in task_b_titles

    @pytest.mark.asyncio
    async def test_list_tasks_performance_large_list(
        self, client: AsyncClient, auth_headers: dict[str, str], db_session: Session, registered_user: User
    ):
        """T057: Test large task list (100+ tasks) loads within 2 seconds."""
        import time

        # Create 100 tasks
        for i in range(100):
            task = Task(user_id=registered_user.id, title=f"Task {i + 1}")
            db_session.add(task)

        db_session.commit()

        # Measure fetch time
        start_time = time.time()
        response = await client.get("/api/v1/tasks", headers=auth_headers)
        elapsed_time = time.time() - start_time

        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 100
        assert elapsed_time < 2.0, f"Task list took {elapsed_time:.2f}s, expected < 2s"

    @pytest.mark.asyncio
    async def test_list_tasks_excludes_archived(
        self, client: AsyncClient, auth_headers: dict[str, str], db_session: Session, registered_user: User
    ):
        """Additional test: Verify archived tasks are excluded from list."""
        # Create active and archived tasks
        active_task = Task(user_id=registered_user.id, title="Active Task", completed=False, is_archived=False)
        archived_task = Task(user_id=registered_user.id, title="Archived Task", completed=True, is_archived=True)

        db_session.add(active_task)
        db_session.add(archived_task)
        db_session.commit()

        # Fetch task list
        response = await client.get("/api/v1/tasks", headers=auth_headers)

        assert response.status_code == 200
        tasks = response.json()

        # Should only have active task
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Active Task"
        assert tasks[0]["is_archived"] is False
