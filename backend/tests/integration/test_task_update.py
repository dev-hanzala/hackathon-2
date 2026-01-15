"""
Integration tests for task update (User Story 5: Update Task).
Tests PUT /api/v1/tasks/{id} endpoint with full user flows.
"""

import pytest
from httpx import AsyncClient


class TestTaskUpdateIntegration:
    """Integration tests for updating task titles."""

    @pytest.mark.asyncio
    async def test_update_task_with_valid_new_title(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test updating task with valid new title returns 200 and persists."""
        # Create task
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Original title"})
        task_id = create_response.json()["id"]

        # Update title
        update_response = await client.put(
            f"/api/v1/tasks/{task_id}", headers=auth_headers, json={"title": "Updated title"}
        )

        assert update_response.status_code == 200
        updated_task = update_response.json()
        assert updated_task["title"] == "Updated title"
        assert updated_task["id"] == task_id

        # Verify update persists
        get_response = await client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
        task = get_response.json()
        assert task["title"] == "Updated title"

    @pytest.mark.asyncio
    async def test_update_task_empty_title_returns_422(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test updating task with empty title returns 422 validation error."""
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Valid title"})
        task_id = create_response.json()["id"]

        response = await client.put(f"/api/v1/tasks/{task_id}", headers=auth_headers, json={"title": ""})

        assert response.status_code == 422

        # Verify title unchanged
        get_response = await client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
        task = get_response.json()
        assert task["title"] == "Valid title"

    @pytest.mark.asyncio
    async def test_update_task_persists_across_sessions(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test update persistence across page reload."""
        # Create and update task
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Original"})
        task_id = create_response.json()["id"]

        await client.put(f"/api/v1/tasks/{task_id}", headers=auth_headers, json={"title": "Persistent update"})

        # Simulate page reload - fetch task again
        list_response = await client.get("/api/v1/tasks", headers=auth_headers)
        tasks = list_response.json()
        task = next(t for t in tasks if t["id"] == task_id)
        assert task["title"] == "Persistent update"

    @pytest.mark.asyncio
    async def test_update_task_user_ownership(self, client: AsyncClient):
        """Test users can only update their own tasks."""
        # Create user 1 and task
        user1_reg = await client.post(
            "/api/v1/auth/register", json={"email": "user1update@example.com", "password": "password123"}
        )
        user1_token = user1_reg.json()["token"]
        user1_headers = {"Authorization": f"Bearer {user1_token}"}

        task_response = await client.post("/api/v1/tasks", headers=user1_headers, json={"title": "User 1's task"})
        task_id = task_response.json()["id"]

        # Create user 2
        user2_reg = await client.post(
            "/api/v1/auth/register", json={"email": "user2update@example.com", "password": "password123"}
        )
        user2_token = user2_reg.json()["token"]
        user2_headers = {"Authorization": f"Bearer {user2_token}"}

        # User 2 tries to update user 1's task - should fail
        update_response = await client.put(f"/api/v1/tasks/{task_id}", headers=user2_headers, json={"title": "Hacked"})
        assert update_response.status_code == 404

        # User 1 can update their own task
        user1_update = await client.put(
            f"/api/v1/tasks/{task_id}", headers=user1_headers, json={"title": "Updated by user 1"}
        )
        assert user1_update.status_code == 200
        assert user1_update.json()["title"] == "Updated by user 1"

    @pytest.mark.asyncio
    async def test_update_task_completion_status_unchanged(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test updating title doesn't change completion status."""
        # Create and complete task
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Task to complete"})
        task_id = create_response.json()["id"]
        await client.patch(f"/api/v1/tasks/{task_id}/complete", headers=auth_headers)

        # Update title
        update_response = await client.put(
            f"/api/v1/tasks/{task_id}", headers=auth_headers, json={"title": "Updated completed task"}
        )

        assert update_response.status_code == 200
        updated_task = update_response.json()
        assert updated_task["title"] == "Updated completed task"
        assert updated_task["completed"] is True  # Completion status unchanged
        assert updated_task["is_archived"] is True  # Archive status unchanged

    @pytest.mark.asyncio
    async def test_update_task_with_special_characters(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test updating task with special characters."""
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Original"})
        task_id = create_response.json()["id"]

        special_titles = [
            "Title with emoji 🎉",
            "Title with <html>tags</html>",
            "Title with 'quotes' and \"double quotes\"",
            "A" * 500,  # Max length
        ]

        for new_title in special_titles:
            response = await client.put(f"/api/v1/tasks/{task_id}", headers=auth_headers, json={"title": new_title})
            assert response.status_code == 200
            assert response.json()["title"] == new_title

    @pytest.mark.asyncio
    async def test_update_task_unauthenticated_returns_401(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test updating task without auth returns 401."""
        # Create task with auth
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Auth test"})
        task_id = create_response.json()["id"]

        # Try to update without auth
        response = await client.put(f"/api/v1/tasks/{task_id}", json={"title": "Unauthorized"})
        assert response.status_code == 401
