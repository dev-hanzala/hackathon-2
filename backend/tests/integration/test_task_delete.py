"""
Integration tests for task deletion (User Story 6: Delete Task).
Tests DELETE /api/v1/tasks/{id} endpoint with full user flows.
"""

import pytest
from httpx import AsyncClient


class TestTaskDeleteIntegration:
    """Integration tests for deleting tasks."""

    @pytest.mark.asyncio
    async def test_delete_task_removes_from_database(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test deleting task removes it from database."""
        # Create task
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Task to delete"})
        task_id = create_response.json()["id"]

        # Delete task
        delete_response = await client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)
        assert delete_response.status_code == 204

        # Verify task no longer exists
        get_response = await client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
        assert get_response.status_code == 404

        # Verify task not in list
        list_response = await client.get("/api/v1/tasks", headers=auth_headers)
        tasks = list_response.json()
        assert not any(t["id"] == task_id for t in tasks)

    @pytest.mark.asyncio
    async def test_deletion_persists_across_sessions(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test deletion persists across page reload."""
        # Create and delete task
        create_response = await client.post(
            "/api/v1/tasks", headers=auth_headers, json={"title": "Persistent deletion"}
        )
        task_id = create_response.json()["id"]
        await client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)

        # Simulate page reload - task should still be deleted
        list_response = await client.get("/api/v1/tasks", headers=auth_headers)
        tasks = list_response.json()
        assert not any(t["id"] == task_id for t in tasks)

    @pytest.mark.asyncio
    async def test_delete_task_user_ownership(self, client: AsyncClient):
        """Test users can only delete their own tasks."""
        # Create user 1 and task
        user1_reg = await client.post(
            "/api/v1/auth/register", json={"email": "user1delete@example.com", "password": "password123"}
        )
        user1_token = user1_reg.json()["token"]
        user1_headers = {"Authorization": f"Bearer {user1_token}"}

        task_response = await client.post("/api/v1/tasks", headers=user1_headers, json={"title": "User 1's task"})
        task_id = task_response.json()["id"]

        # Create user 2
        user2_reg = await client.post(
            "/api/v1/auth/register", json={"email": "user2delete@example.com", "password": "password123"}
        )
        user2_token = user2_reg.json()["token"]
        user2_headers = {"Authorization": f"Bearer {user2_token}"}

        # User 2 tries to delete user 1's task - should fail
        delete_response = await client.delete(f"/api/v1/tasks/{task_id}", headers=user2_headers)
        assert delete_response.status_code == 404

        # Task should still exist for user 1
        user1_get = await client.get(f"/api/v1/tasks/{task_id}", headers=user1_headers)
        assert user1_get.status_code == 200

        # User 1 can delete their own task
        user1_delete = await client.delete(f"/api/v1/tasks/{task_id}", headers=user1_headers)
        assert user1_delete.status_code == 204

    @pytest.mark.asyncio
    async def test_delete_confirmation_workflow(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test delete confirmation workflow (server-side logic)."""
        # Create task
        create_response = await client.post(
            "/api/v1/tasks", headers=auth_headers, json={"title": "Task requiring confirmation"}
        )
        task_id = create_response.json()["id"]

        # First attempt - should succeed (no confirmation required at API level)
        delete_response = await client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)
        assert delete_response.status_code == 204

        # Second delete attempt should fail (already deleted)
        second_delete = await client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)
        assert second_delete.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_completed_task(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test deleting completed tasks works."""
        # Create and complete task
        create_response = await client.post(
            "/api/v1/tasks", headers=auth_headers, json={"title": "Completed task to delete"}
        )
        task_id = create_response.json()["id"]
        await client.patch(f"/api/v1/tasks/{task_id}/complete", headers=auth_headers)

        # Delete should succeed
        delete_response = await client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)
        assert delete_response.status_code == 204

        # Verify deletion
        get_response = await client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_task_unauthenticated_returns_401(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test deleting task without auth returns 401."""
        # Create task with auth
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Auth test task"})
        task_id = create_response.json()["id"]

        # Try to delete without auth
        response = await client.delete(f"/api/v1/tasks/{task_id}")
        assert response.status_code == 401

        # Task should still exist
        get_response = await client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
        assert get_response.status_code == 200
