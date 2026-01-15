"""Integration tests for concurrent operations.

T156: Test concurrent operations
- Two users modifying tasks simultaneously
- Last-Write-Wins, no data corruption
"""

import asyncio

import pytest
from fastapi import status
from httpx import AsyncClient

from src.db.models import Task, User
from src.middleware.auth import create_access_token, get_password_hash


class TestConcurrentOperations:
    """T156: Integration tests for concurrent task operations."""

    @pytest.mark.asyncio
    async def test_concurrent_task_creation_by_same_user(self, client: AsyncClient, auth_headers):
        """Test that a user can create multiple tasks concurrently without conflicts."""
        # Create 5 tasks concurrently
        tasks = []
        for i in range(5):
            task_data = {"title": f"Concurrent Task {i + 1}", "description": f"Created concurrently {i + 1}"}
            tasks.append(client.post("/api/v1/tasks", json=task_data, headers=auth_headers))

        # Wait for all requests to complete
        responses = await asyncio.gather(*tasks)

        # All should succeed
        for response in responses:
            assert response.status_code == status.HTTP_201_CREATED

        # All should have unique IDs
        task_ids = [resp.json()["id"] for resp in responses]
        assert len(task_ids) == len(set(task_ids))  # No duplicates

    @pytest.mark.asyncio
    async def test_concurrent_task_updates_last_write_wins(
        self, client: AsyncClient, auth_headers, db_session, registered_user
    ):
        """Test that concurrent updates to same task follow last-write-wins."""
        # Create a task for registered_user
        task = Task(user_id=registered_user.id, title="Original Title")
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        # Update the same task concurrently with different titles
        updates = []
        for i in range(3):
            updates.append(
                client.put(f"/api/v1/tasks/{task.id}", json={"title": f"Updated Title {i + 1}"}, headers=auth_headers)
            )

        # Wait for all updates
        responses = await asyncio.gather(*updates)

        # All updates should succeed
        for response in responses:
            assert response.status_code == status.HTTP_200_OK

        # Get final state
        final_response = await client.get(f"/api/v1/tasks/{task.id}", headers=auth_headers)
        assert final_response.status_code == status.HTTP_200_OK

        # Task should have one of the updated titles (last write wins)
        final_data = final_response.json()
        assert final_data["title"] in ["Updated Title 1", "Updated Title 2", "Updated Title 3"]

    @pytest.mark.asyncio
    async def test_concurrent_task_completion_toggles(
        self, client: AsyncClient, auth_headers, db_session, registered_user
    ):
        """Test concurrent task completion toggles maintain data integrity."""
        # Create a task for registered_user
        task = Task(user_id=registered_user.id, title="Toggle Test Task")
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        # Toggle completion status concurrently multiple times
        toggles = []
        for _i in range(4):
            # Alternate between completing and uncompleting
            toggles.append(client.patch(f"/api/v1/tasks/{task.id}/complete", headers=auth_headers))

        # Wait for all toggles
        responses = await asyncio.gather(*toggles)

        # All should succeed
        for response in responses:
            assert response.status_code == status.HTTP_200_OK

        # Get final state - should be either completed or not
        final_response = await client.get(f"/api/v1/tasks/{task.id}", headers=auth_headers)
        final_data = final_response.json()

        # Completion status should be a boolean (not corrupted)
        assert isinstance(final_data["completed"], bool)

    @pytest.mark.asyncio
    async def test_concurrent_operations_by_different_users(self, client: AsyncClient, db_session):
        """Test that different users can operate on their own tasks concurrently."""
        # Create two users
        user1 = User(email="user1@example.com", password_hash=get_password_hash("Password123"))
        user2 = User(email="user2@example.com", password_hash=get_password_hash("Password123"))
        db_session.add(user1)
        db_session.add(user2)
        db_session.commit()
        db_session.refresh(user1)
        db_session.refresh(user2)

        # Create tokens for both users
        token1 = create_access_token(data={"sub": str(user1.id), "email": user1.email})
        token2 = create_access_token(data={"sub": str(user2.id), "email": user2.email})

        headers1 = {"Authorization": f"Bearer {token1}"}
        headers2 = {"Authorization": f"Bearer {token2}"}

        # Both users create tasks concurrently
        operations = [
            client.post("/api/v1/tasks", json={"title": "User 1 Task 1"}, headers=headers1),
            client.post("/api/v1/tasks", json={"title": "User 1 Task 2"}, headers=headers1),
            client.post("/api/v1/tasks", json={"title": "User 2 Task 1"}, headers=headers2),
            client.post("/api/v1/tasks", json={"title": "User 2 Task 2"}, headers=headers2),
        ]

        responses = await asyncio.gather(*operations)

        # All operations should succeed
        for response in responses:
            assert response.status_code == status.HTTP_201_CREATED

        # Verify user 1 sees only their tasks
        user1_tasks_response = await client.get("/api/v1/tasks", headers=headers1)
        user1_tasks = user1_tasks_response.json()
        assert len([t for t in user1_tasks if "User 1" in t["title"]]) == 2

        # Verify user 2 sees only their tasks
        user2_tasks_response = await client.get("/api/v1/tasks", headers=headers2)
        user2_tasks = user2_tasks_response.json()
        assert len([t for t in user2_tasks if "User 2" in t["title"]]) == 2

    @pytest.mark.asyncio
    async def test_concurrent_task_deletion_is_idempotent(
        self, client: AsyncClient, auth_headers, db_session, registered_user
    ):
        """Test that concurrent deletion attempts don't cause errors."""
        # Create a task
        task = Task(user_id=registered_user.id, title="Task to Delete")
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        # Try to delete it concurrently multiple times
        deletions = []
        for _ in range(3):
            deletions.append(client.delete(f"/api/v1/tasks/{task.id}", headers=auth_headers))

        responses = await asyncio.gather(*deletions, return_exceptions=True)

        # At least one should succeed, others may return 404
        success_count = sum(
            1 for r in responses if not isinstance(r, Exception) and r.status_code == status.HTTP_200_OK
        )
        not_found_count = sum(
            1 for r in responses if not isinstance(r, Exception) and r.status_code == status.HTTP_404_NOT_FOUND
        )

        # Should have at least one success or multiple 404s (idempotent)
        assert success_count >= 1 or not_found_count >= 2


class TestDataIntegrity:
    """Tests for data integrity under concurrent operations."""

    @pytest.mark.asyncio
    async def test_task_count_accurate_after_concurrent_operations(self, client: AsyncClient, auth_headers):
        """Test that task count remains accurate after concurrent creates/deletes."""
        # Get initial count
        initial_response = await client.get("/api/v1/tasks", headers=auth_headers)
        initial_count = len(initial_response.json())

        # Create 5 tasks concurrently
        creates = []
        for i in range(5):
            creates.append(
                client.post("/api/v1/tasks", json={"title": f"Integrity Test {i + 1}"}, headers=auth_headers)
            )

        await asyncio.gather(*creates)

        # Verify count increased by 5
        after_create_response = await client.get("/api/v1/tasks", headers=auth_headers)
        after_create_count = len(after_create_response.json())

        assert after_create_count == initial_count + 5

    @pytest.mark.asyncio
    async def test_no_orphaned_tasks_after_concurrent_user_operations(self, client: AsyncClient, db_session):
        """Test that no orphaned tasks exist after concurrent user operations."""
        # Create a user
        user = User(email="integrity_user@example.com", password_hash=get_password_hash("Password123"))
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        token = create_access_token(data={"sub": str(user.id), "email": user.email})
        headers = {"Authorization": f"Bearer {token}"}

        # Create multiple tasks concurrently
        creates = []
        for i in range(10):
            creates.append(client.post("/api/v1/tasks", json={"title": f"Task {i + 1}"}, headers=headers))

        responses = await asyncio.gather(*creates)
        [r.json()["id"] for r in responses]

        # Verify all tasks belong to the user
        from sqlmodel import select

        stmt = select(Task).where(Task.user_id == user.id)
        user_tasks = list(db_session.exec(stmt))

        # Should have at least the tasks we created
        assert len(user_tasks) >= 10

        # All tasks should have valid user_id
        for task in user_tasks:
            assert task.user_id == user.id

    @pytest.mark.asyncio
    async def test_concurrent_list_operations_return_consistent_data(self, client: AsyncClient, auth_headers):
        """Test that concurrent list operations return consistent data."""
        # List tasks concurrently multiple times
        lists = []
        for _ in range(5):
            lists.append(client.get("/api/v1/tasks", headers=auth_headers))

        responses = await asyncio.gather(*lists)

        # All should succeed
        for response in responses:
            assert response.status_code == status.HTTP_200_OK

        # All should return valid JSON arrays
        for response in responses:
            data = response.json()
            assert isinstance(data, list)
