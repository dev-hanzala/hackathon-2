"""
Integration tests for task completion (User Story 4: Mark Complete).
Tests PATCH /api/v1/tasks/{id}/complete and /incomplete endpoints with full user flows.
"""

import pytest
from httpx import AsyncClient


class TestTaskCompleteIntegration:
    """Integration tests for marking tasks complete/incomplete."""

    @pytest.mark.asyncio
    async def test_mark_task_complete_persists_and_archives(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test marking task complete sets completed=true, is_archived=true and persists."""
        # Create task
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Task to complete"})
        task_id = create_response.json()["id"]

        # Mark as complete
        complete_response = await client.patch(f"/api/v1/tasks/{task_id}/complete", headers=auth_headers)
        assert complete_response.status_code == 200
        completed_task = complete_response.json()
        assert completed_task["completed"] is True
        assert completed_task["is_archived"] is True

        # Verify task no longer appears in active task list
        list_response = await client.get("/api/v1/tasks", headers=auth_headers)
        tasks = list_response.json()
        assert not any(t["id"] == task_id for t in tasks)

    @pytest.mark.asyncio
    async def test_mark_task_incomplete_unarchives(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test marking task incomplete sets completed=false, is_archived=false."""
        # Create and complete task
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Task to toggle"})
        task_id = create_response.json()["id"]
        await client.patch(f"/api/v1/tasks/{task_id}/complete", headers=auth_headers)

        # Mark as incomplete
        incomplete_response = await client.patch(f"/api/v1/tasks/{task_id}/incomplete", headers=auth_headers)
        assert incomplete_response.status_code == 200
        uncompleted_task = incomplete_response.json()
        assert uncompleted_task["completed"] is False
        assert uncompleted_task["is_archived"] is False

        # Verify task reappears in active task list
        list_response = await client.get("/api/v1/tasks", headers=auth_headers)
        tasks = list_response.json()
        assert any(t["id"] == task_id and t["title"] == "Task to toggle" for t in tasks)

    @pytest.mark.asyncio
    async def test_completion_persists_across_sessions(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test completion status persists across page reload."""
        # Create and complete task
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Persistent task"})
        task_id = create_response.json()["id"]
        await client.patch(f"/api/v1/tasks/{task_id}/complete", headers=auth_headers)

        # Get specific task to verify status persists
        get_response = await client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
        task = get_response.json()
        assert task["completed"] is True
        assert task["is_archived"] is True

    @pytest.mark.asyncio
    async def test_complete_task_user_ownership(self, client: AsyncClient):
        """Test users can only complete their own tasks."""
        # Create user 1 and task
        user1_reg = await client.post(
            "/api/v1/auth/register", json={"email": "user1complete@example.com", "password": "password123"}
        )
        user1_token = user1_reg.json()["token"]
        user1_headers = {"Authorization": f"Bearer {user1_token}"}

        task_response = await client.post("/api/v1/tasks", headers=user1_headers, json={"title": "User 1's task"})
        task_id = task_response.json()["id"]

        # Create user 2
        user2_reg = await client.post(
            "/api/v1/auth/register", json={"email": "user2complete@example.com", "password": "password123"}
        )
        user2_token = user2_reg.json()["token"]
        user2_headers = {"Authorization": f"Bearer {user2_token}"}

        # User 2 tries to complete user 1's task - should fail
        complete_response = await client.patch(f"/api/v1/tasks/{task_id}/complete", headers=user2_headers)
        assert complete_response.status_code == 404

        # User 1 can complete their own task
        user1_complete = await client.patch(f"/api/v1/tasks/{task_id}/complete", headers=user1_headers)
        assert user1_complete.status_code == 200

    @pytest.mark.asyncio
    async def test_concurrent_completion_last_write_wins(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test concurrent completion operations (Last-Write-Wins)."""
        # Create task
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Concurrent task"})
        task_id = create_response.json()["id"]

        # Simulate concurrent operations
        response1 = await client.patch(f"/api/v1/tasks/{task_id}/complete", headers=auth_headers)
        response2 = await client.patch(f"/api/v1/tasks/{task_id}/incomplete", headers=auth_headers)

        # Both should succeed (Last-Write-Wins)
        assert response1.status_code == 200
        assert response2.status_code == 200

        # Final state should be incomplete (last write)
        get_response = await client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
        task = get_response.json()
        assert task["completed"] is False

    @pytest.mark.asyncio
    async def test_complete_unauthenticated_returns_401(self, client: AsyncClient, auth_headers: dict[str, str]):
        """Test completing task without auth returns 401."""
        # Create task with auth
        create_response = await client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Auth test task"})
        task_id = create_response.json()["id"]

        # Try to complete without auth
        response = await client.patch(f"/api/v1/tasks/{task_id}/complete")
        assert response.status_code == 401
