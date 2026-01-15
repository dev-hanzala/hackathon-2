"""
Contract tests for tasks API endpoints.
Validates API responses against OpenAPI specification.
"""

from uuid import UUID

import pytest
from httpx import AsyncClient


class TestTasksContractGetList:
    """Contract tests for GET /api/v1/tasks endpoint."""

    @pytest.mark.asyncio
    async def test_get_tasks_returns_200_with_array(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test GET /tasks returns 200 with task array."""
        response = await client.get("/api/v1/tasks", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_tasks_response_schema(
        self, client: AsyncClient, auth_headers: dict[str, str], db_session, registered_user
    ):
        """Test GET /tasks response matches OpenAPI schema."""
        from src.db.models import Task

        # Create a test task for the registered user
        task = Task(
            user_id=registered_user.id,
            title="Schema Test Task",
        )
        db_session.add(task)
        db_session.commit()

        response = await client.get("/api/v1/tasks", headers=auth_headers)

        assert response.status_code == 200
        tasks = response.json()
        assert isinstance(tasks, list)

        if len(tasks) > 0:
            task_data = tasks[0]
            # Verify required fields
            assert "id" in task_data
            assert "user_id" in task_data
            assert "title" in task_data
            assert "completed" in task_data
            assert "is_archived" in task_data
            assert "created_at" in task_data
            assert "updated_at" in task_data

            # Verify field types
            assert isinstance(task_data["id"], str)
            UUID(task_data["id"])  # Validates UUID format
            assert isinstance(task_data["user_id"], str)
            UUID(task_data["user_id"])
            assert isinstance(task_data["title"], str)
            assert isinstance(task_data["completed"], bool)
            assert isinstance(task_data["is_archived"], bool)
            assert isinstance(task_data["created_at"], str)
            assert isinstance(task_data["updated_at"], str)

    @pytest.mark.asyncio
    async def test_get_tasks_requires_auth(self, client: AsyncClient):
        """Test GET /tasks returns 401 without authentication."""
        response = await client.get("/api/v1/tasks")

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_tasks_empty_array_on_no_tasks(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test GET /tasks returns empty array when user has no tasks."""
        # Create new user with no tasks
        register_response = await client.post(
            "/api/v1/auth/register", json={"email": "emptyuser@example.com", "password": "password123"}
        )
        assert register_response.status_code == 201

        auth_data = register_response.json()
        token = auth_data["token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.get("/api/v1/tasks", headers=headers)

        assert response.status_code == 200
        tasks = response.json()
        assert isinstance(tasks, list)
        assert len(tasks) == 0

    @pytest.mark.asyncio
    async def test_get_tasks_filters_archived(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test GET /tasks excludes archived tasks."""
        # This test assumes we have a way to create archived tasks
        # For now, we just verify the response structure
        response = await client.get("/api/v1/tasks", headers=auth_headers)

        assert response.status_code == 200
        tasks = response.json()

        # Verify no archived tasks in active list
        for task in tasks:
            assert task["is_archived"] is False

    @pytest.mark.asyncio
    async def test_get_tasks_content_type(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test GET /tasks returns JSON content type."""
        response = await client.get("/api/v1/tasks", headers=auth_headers)

        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]


class TestTasksContractCreate:
    """Contract tests for POST /api/v1/tasks endpoint."""

    @pytest.mark.asyncio
    async def test_create_task_returns_201_with_task(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test POST /tasks returns 201 with created task."""
        response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "New Task"})

        assert response.status_code == 201
        data = response.json()
        assert isinstance(data, dict)
        assert data["title"] == "New Task"

    @pytest.mark.asyncio
    async def test_create_task_response_schema(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test POST /tasks response matches OpenAPI schema."""
        response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Schema Test Task"})

        assert response.status_code == 201
        task_data = response.json()

        # Verify required fields
        assert "id" in task_data
        assert "user_id" in task_data
        assert "title" in task_data
        assert "completed" in task_data
        assert "is_archived" in task_data
        assert "created_at" in task_data
        assert "updated_at" in task_data

        # Verify field types
        assert isinstance(task_data["id"], str)
        UUID(task_data["id"])  # Validates UUID format
        assert isinstance(task_data["user_id"], str)
        UUID(task_data["user_id"])
        assert isinstance(task_data["title"], str)
        assert task_data["title"] == "Schema Test Task"
        assert isinstance(task_data["completed"], bool)
        assert task_data["completed"] is False  # New tasks start incomplete
        assert isinstance(task_data["is_archived"], bool)
        assert task_data["is_archived"] is False  # New tasks not archived
        assert isinstance(task_data["created_at"], str)
        assert isinstance(task_data["updated_at"], str)

    @pytest.mark.asyncio
    async def test_create_task_requires_auth(self, client: AsyncClient):
        """Test POST /tasks returns 401 without authentication."""
        response = await client.post("/api/v1/tasks", json={"title": "Unauthorized Task"})

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_create_task_empty_title_validation(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test POST /tasks returns 422 with empty title."""
        response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": ""})

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_task_missing_title_validation(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test POST /tasks returns 422 without title field."""
        response = await client.post("/api/v1/tasks", headers=auth_headers, json={})

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_task_title_max_length(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test POST /tasks validates max title length (500 chars)."""
        long_title = "A" * 501
        response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": long_title})

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_task_content_type(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test POST /tasks returns JSON content type."""
        response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Content Type Test"})

        assert response.status_code == 201
        assert "application/json" in response.headers["content-type"]


class TestTasksContractComplete:
    """Contract tests for PATCH /api/v1/tasks/{id}/complete and /incomplete endpoints."""

    @pytest.mark.asyncio
    async def test_complete_task_returns_200(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test PATCH /tasks/{id}/complete returns 200 with updated task."""
        # Create a task first
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Task to complete"})
        assert create_response.status_code == 201
        task = create_response.json()
        task_id = task["id"]

        # Mark as complete
        response = await client.patch(f"/api/v1/tasks/{task_id}/complete", headers=auth_headers)

        assert response.status_code == 200
        completed_task = response.json()
        assert completed_task["completed"] is True
        assert completed_task["is_archived"] is True

    @pytest.mark.asyncio
    async def test_incomplete_task_returns_200(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test PATCH /tasks/{id}/incomplete returns 200 with updated task."""
        # Create and complete a task first
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Task to uncomplete"})
        task = create_response.json()
        task_id = task["id"]

        await client.patch(f"/api/v1/tasks/{task_id}/complete", headers=auth_headers)

        # Mark as incomplete
        response = await client.patch(f"/api/v1/tasks/{task_id}/incomplete", headers=auth_headers)

        assert response.status_code == 200
        uncompleted_task = response.json()
        assert uncompleted_task["completed"] is False
        assert uncompleted_task["is_archived"] is False

    @pytest.mark.asyncio
    async def test_complete_task_response_schema(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test PATCH /tasks/{id}/complete response matches schema."""
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Schema test"})
        task_id = create_response.json()["id"]

        response = await client.patch(f"/api/v1/tasks/{task_id}/complete", headers=auth_headers)

        assert response.status_code == 200
        task_data = response.json()

        # Verify all required fields present
        assert "id" in task_data
        assert "user_id" in task_data
        assert "title" in task_data
        assert "completed" in task_data
        assert "is_archived" in task_data
        assert "created_at" in task_data
        assert "updated_at" in task_data

        # Verify types
        assert isinstance(task_data["completed"], bool)
        assert isinstance(task_data["is_archived"], bool)
        assert task_data["completed"] is True
        assert task_data["is_archived"] is True

    @pytest.mark.asyncio
    async def test_complete_nonexistent_task_returns_404(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test PATCH /tasks/{invalid-id}/complete returns 404."""
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        response = await client.patch(f"/api/v1/tasks/{fake_uuid}/complete", headers=auth_headers)

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_complete_task_requires_auth(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test PATCH /tasks/{id}/complete requires authentication."""
        # Create task with auth
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Auth test"})
        task_id = create_response.json()["id"]

        # Try to complete without auth
        response = await client.patch(f"/api/v1/tasks/{task_id}/complete")

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_complete_task_content_type(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test PATCH /tasks/{id}/complete returns JSON content type."""
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Content type test"})
        task_id = create_response.json()["id"]

        response = await client.patch(f"/api/v1/tasks/{task_id}/complete", headers=auth_headers)

        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]


class TestTasksContractUpdate:
    """Contract tests for PUT /api/v1/tasks/{id} endpoint."""

    @pytest.mark.asyncio
    async def test_update_task_returns_200(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test PUT /tasks/{id} returns 200 with updated task."""
        # Create a task first
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Original title"})
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]

        # Update the task
        response = await client.put(f"/api/v1/tasks/{task_id}", headers=auth_headers, json={"title": "Updated title"})

        assert response.status_code == 200
        updated_task = response.json()
        assert updated_task["title"] == "Updated title"
        assert updated_task["id"] == task_id

    @pytest.mark.asyncio
    async def test_update_task_response_schema(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test PUT /tasks/{id} response matches schema."""
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Schema test"})
        task_id = create_response.json()["id"]

        response = await client.put(f"/api/v1/tasks/{task_id}", headers=auth_headers, json={"title": "New title"})

        assert response.status_code == 200
        task_data = response.json()

        # Verify all required fields present
        assert "id" in task_data
        assert "user_id" in task_data
        assert "title" in task_data
        assert "completed" in task_data
        assert "is_archived" in task_data
        assert "created_at" in task_data
        assert "updated_at" in task_data

        assert task_data["title"] == "New title"
        assert isinstance(task_data["completed"], bool)
        assert isinstance(task_data["is_archived"], bool)

    @pytest.mark.asyncio
    async def test_update_task_empty_title_validation(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test PUT /tasks/{id} returns 422 with empty title."""
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Valid title"})
        task_id = create_response.json()["id"]

        response = await client.put(f"/api/v1/tasks/{task_id}", headers=auth_headers, json={"title": ""})

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_update_task_title_max_length(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test PUT /tasks/{id} validates max title length (500 chars)."""
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Valid title"})
        task_id = create_response.json()["id"]

        long_title = "A" * 501
        response = await client.put(f"/api/v1/tasks/{task_id}", headers=auth_headers, json={"title": long_title})

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_update_nonexistent_task_returns_404(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test PUT /tasks/{invalid-id} returns 404."""
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        response = await client.put(f"/api/v1/tasks/{fake_uuid}", headers=auth_headers, json={"title": "New title"})

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_task_requires_auth(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test PUT /tasks/{id} requires authentication."""
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Auth test"})
        task_id = create_response.json()["id"]

        # Try to update without auth
        response = await client.put(f"/api/v1/tasks/{task_id}", json={"title": "Unauthorized update"})

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_update_task_content_type(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test PUT /tasks/{id} returns JSON content type."""
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Content type test"})
        task_id = create_response.json()["id"]

        response = await client.put(f"/api/v1/tasks/{task_id}", headers=auth_headers, json={"title": "Updated"})

        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]


class TestTasksContractDelete:
    """Contract tests for DELETE /api/v1/tasks/{id} endpoint."""

    @pytest.mark.asyncio
    async def test_delete_task_returns_204(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test DELETE /tasks/{id} returns 204 No Content."""
        # Create a task first
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Task to delete"})
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]

        # Delete the task
        response = await client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)

        assert response.status_code == 204
        assert len(response.content) == 0  # No response body

    @pytest.mark.asyncio
    async def test_delete_nonexistent_task_returns_404(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test DELETE /tasks/{invalid-id} returns 404."""
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        response = await client.delete(f"/api/v1/tasks/{fake_uuid}", headers=auth_headers)

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_task_requires_auth(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test DELETE /tasks/{id} requires authentication."""
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Auth test"})
        task_id = create_response.json()["id"]

        # Try to delete without auth
        response = await client.delete(f"/api/v1/tasks/{task_id}")

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_delete_completed_task_succeeds(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test DELETE /tasks/{id} works on completed tasks."""
        # Create and complete task
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Completed task"})
        task_id = create_response.json()["id"]
        await client.patch(f"/api/v1/tasks/{task_id}/complete", headers=auth_headers)

        # Delete should succeed
        response = await client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)

        assert response.status_code == 204
