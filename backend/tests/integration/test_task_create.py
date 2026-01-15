"""
Integration tests for task creation (User Story 3: Add Task).
Tests POST /api/v1/tasks endpoint with full user flows.
"""

import pytest
from httpx import AsyncClient


class TestTaskCreateIntegration:
    """Integration tests for creating tasks."""

    @pytest.mark.asyncio
    async def test_create_task_with_valid_title(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test creating a task with valid title returns 201 and persists to database."""
        # Create task
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Buy groceries"})

        assert create_response.status_code == 201
        created_task = create_response.json()
        assert created_task["title"] == "Buy groceries"
        assert created_task["completed"] is False
        assert created_task["is_archived"] is False
        task_id = created_task["id"]

        # Verify task appears in list
        list_response = await client.get("/api/v1/tasks", headers=auth_headers)
        assert list_response.status_code == 200
        tasks = list_response.json()
        assert any(t["id"] == task_id and t["title"] == "Buy groceries" for t in tasks)

    @pytest.mark.asyncio
    async def test_create_task_empty_title_returns_422(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test creating task with empty title returns 422 validation error."""
        response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": ""})

        assert response.status_code == 422
        error_data = response.json()
        assert "detail" in error_data

        # Verify no task was created
        list_response = await client.get("/api/v1/tasks", headers=auth_headers)
        tasks = list_response.json()
        assert not any(t["title"] == "" for t in tasks)

    @pytest.mark.asyncio
    async def test_create_multiple_tasks_rapid_succession(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test creating multiple tasks rapidly generates unique IDs and persists all."""
        task_titles = ["Task 1", "Task 2", "Task 3", "Task 4", "Task 5"]
        created_tasks = []

        # Create tasks in rapid succession
        for title in task_titles:
            response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": title})
            assert response.status_code == 201
            created_tasks.append(response.json())

        # Verify all have unique IDs
        task_ids = [t["id"] for t in created_tasks]
        assert len(task_ids) == len(set(task_ids))  # All unique

        # Verify all appear in list
        list_response = await client.get("/api/v1/tasks", headers=auth_headers)
        tasks = list_response.json()
        for title in task_titles:
            assert any(t["title"] == title for t in tasks)

    @pytest.mark.asyncio
    async def test_create_task_unauthenticated_returns_401(self, client: AsyncClient):
        """Test creating task without auth token returns 401."""
        response = await client.post("/api/v1/tasks", json={"title": "Unauthorized task"})

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_create_task_with_special_characters(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test creating task with special characters and long strings."""
        special_titles = [
            "Task with emoji 🚀",
            "Task with <html>tags</html>",
            "Task with 'quotes' and \"double quotes\"",
            "Task with newline\ncharacter",
            "A" * 500,  # Max length (500 chars)
        ]

        for title in special_titles:
            response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": title})
            assert response.status_code == 201
            created_task = response.json()
            assert created_task["title"] == title

    @pytest.mark.asyncio
    async def test_create_task_user_isolation(self, client: AsyncClient):
        """Test tasks are isolated to the creating user."""
        # Create user 1
        user1_reg = await client.post(
            "/api/v1/auth/register", json={"email": "user1@example.com", "password": "password123"}
        )
        assert user1_reg.status_code == 201
        user1_token = user1_reg.json()["token"]
        user1_headers = {"Authorization": f"Bearer {user1_token}"}

        # Create user 2
        user2_reg = await client.post(
            "/api/v1/auth/register", json={"email": "user2@example.com", "password": "password123"}
        )
        assert user2_reg.status_code == 201
        user2_token = user2_reg.json()["token"]
        user2_headers = {"Authorization": f"Bearer {user2_token}"}

        # User 1 creates a task
        task_response = await client.post("/api/v1/tasks", headers=user1_headers, json={"title": "User 1's task"})
        assert task_response.status_code == 201

        # User 2 should NOT see user 1's task
        user2_tasks_response = await client.get("/api/v1/tasks", headers=user2_headers)
        user2_tasks = user2_tasks_response.json()
        assert not any(t["title"] == "User 1's task" for t in user2_tasks)

        # User 1 should see their own task
        user1_tasks_response = await client.get("/api/v1/tasks", headers=user1_headers)
        user1_tasks = user1_tasks_response.json()
        assert any(t["title"] == "User 1's task" for t in user1_tasks)
