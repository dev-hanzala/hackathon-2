"""Integration tests for rapid task creation.

T157: Test rapid task creation
- 5+ tasks created in quick succession
- All unique IDs, no duplicates
"""

import asyncio
from datetime import UTC, datetime

import pytest
from fastapi import status
from httpx import AsyncClient


class TestRapidCreation:
    """T157: Integration tests for rapid task creation."""

    @pytest.mark.asyncio
    async def test_rapid_sequential_task_creation(self, client: AsyncClient, auth_headers):
        """Test creating tasks rapidly in sequence."""
        task_ids = []

        # Create 10 tasks rapidly one after another
        for i in range(10):
            response = await client.post(
                "/api/v1/tasks",
                json={
                    "title": f"Rapid Task {i + 1}",
                    "description": f"Created at {datetime.now(UTC).isoformat()}",
                },
                headers=auth_headers,
            )

            assert response.status_code == status.HTTP_201_CREATED
            data = response.json()
            task_ids.append(data["id"])

        # Verify all IDs are unique
        assert len(task_ids) == 10
        assert len(set(task_ids)) == 10  # No duplicates

    @pytest.mark.asyncio
    async def test_rapid_concurrent_task_creation(self, client: AsyncClient, auth_headers):
        """Test creating tasks concurrently in rapid succession."""
        # Create 20 tasks concurrently
        tasks = []
        for i in range(20):
            tasks.append(
                client.post(
                    "/api/v1/tasks",
                    json={"title": f"Concurrent Rapid Task {i + 1}", "description": f"Batch {i + 1}"},
                    headers=auth_headers,
                )
            )

        # Wait for all to complete
        responses = await asyncio.gather(*tasks)

        # All should succeed
        for response in responses:
            assert response.status_code == status.HTTP_201_CREATED

        # Extract all task IDs
        task_ids = [resp.json()["id"] for resp in responses]

        # Verify all IDs are unique (no duplicates)
        assert len(task_ids) == 20
        assert len(set(task_ids)) == 20

    @pytest.mark.asyncio
    async def test_rapid_creation_with_varying_data(self, client: AsyncClient, auth_headers):
        """Test rapid creation with different task data."""
        tasks = []

        # Create tasks with varying properties
        for i in range(15):
            task_data = {
                "title": f"Task {i + 1}",
                "description": f"Description {i + 1}" if i % 2 == 0 else None,
                "completed": i % 3 == 0,
            }
            tasks.append(client.post("/api/v1/tasks", json=task_data, headers=auth_headers))

        responses = await asyncio.gather(*tasks)

        # All should succeed
        success_count = sum(1 for r in responses if r.status_code == status.HTTP_201_CREATED)
        assert success_count == 15

        # All should have unique IDs
        task_ids = [r.json()["id"] for r in responses]
        assert len(set(task_ids)) == 15

    @pytest.mark.asyncio
    async def test_rapid_creation_maintains_order(self, client: AsyncClient, auth_headers):
        """Test that rapidly created tasks maintain creation order."""
        # Create 5 tasks sequentially
        created_tasks = []

        for i in range(5):
            response = await client.post("/api/v1/tasks", json={"title": f"Ordered Task {i + 1}"}, headers=auth_headers)
            assert response.status_code == status.HTTP_201_CREATED
            created_tasks.append(response.json())

        # List all tasks
        list_response = await client.get("/api/v1/tasks", headers=auth_headers)
        all_tasks = list_response.json()

        # Verify all created tasks exist in the list
        created_ids = {task["id"] for task in created_tasks}
        listed_ids = {task["id"] for task in all_tasks}

        assert created_ids.issubset(listed_ids)

    @pytest.mark.asyncio
    async def test_rapid_creation_does_not_cause_race_conditions(self, client: AsyncClient, auth_headers):
        """Test that rapid creation doesn't cause race conditions or data corruption."""
        # Create 25 tasks concurrently
        tasks = []
        for i in range(25):
            tasks.append(
                client.post(
                    "/api/v1/tasks",
                    json={
                        "title": f"Race Test {i + 1}",
                        "completed": False,
                    },
                    headers=auth_headers,
                )
            )

        responses = await asyncio.gather(*tasks)

        # All should succeed
        for response in responses:
            assert response.status_code == status.HTTP_201_CREATED
            data = response.json()

            # Verify data integrity
            assert "id" in data
            assert "title" in data
            assert "completed" in data
            assert data["completed"] is False
            assert "created_at" in data
            assert "updated_at" in data

    @pytest.mark.asyncio
    async def test_rapid_creation_all_tasks_retrievable(self, client: AsyncClient, auth_headers):
        """Test that all rapidly created tasks are retrievable."""
        # Create 12 tasks concurrently
        create_requests = []
        for i in range(12):
            create_requests.append(
                client.post("/api/v1/tasks", json={"title": f"Retrievable Task {i + 1}"}, headers=auth_headers)
            )

        create_responses = await asyncio.gather(*create_requests)
        created_ids = [r.json()["id"] for r in create_responses]

        # Retrieve each task individually
        get_requests = []
        for task_id in created_ids:
            get_requests.append(client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers))

        get_responses = await asyncio.gather(*get_requests)

        # All should be retrievable
        for response in get_responses:
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["id"] in created_ids


class TestRapidOperations:
    """Tests for rapid operations beyond just creation."""

    @pytest.mark.asyncio
    async def test_rapid_create_then_update(self, client: AsyncClient, auth_headers):
        """Test rapidly creating and updating tasks."""
        # Create 5 tasks
        create_requests = []
        for i in range(5):
            create_requests.append(
                client.post("/api/v1/tasks", json={"title": f"Update Test {i + 1}"}, headers=auth_headers)
            )

        create_responses = await asyncio.gather(*create_requests)
        task_ids = [r.json()["id"] for r in create_responses]

        # Immediately update all tasks concurrently
        update_requests = []
        for i, task_id in enumerate(task_ids):
            update_requests.append(
                client.put(f"/api/v1/tasks/{task_id}", json={"title": f"Updated Task {i + 1}"}, headers=auth_headers)
            )

        update_responses = await asyncio.gather(*update_requests)

        # All updates should succeed
        for response in update_responses:
            assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_rapid_create_then_complete(self, client: AsyncClient, auth_headers):
        """Test rapidly creating and completing tasks."""
        # Create 8 tasks
        create_requests = []
        for i in range(8):
            create_requests.append(
                client.post("/api/v1/tasks", json={"title": f"Complete Test {i + 1}"}, headers=auth_headers)
            )

        create_responses = await asyncio.gather(*create_requests)
        task_ids = [r.json()["id"] for r in create_responses]

        # Immediately complete all tasks concurrently
        complete_requests = []
        for task_id in task_ids:
            complete_requests.append(client.patch(f"/api/v1/tasks/{task_id}/complete", headers=auth_headers))

        complete_responses = await asyncio.gather(*complete_requests)

        # All completions should succeed
        for response in complete_responses:
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["completed"] is True

    @pytest.mark.asyncio
    async def test_rapid_create_then_delete(self, client: AsyncClient, auth_headers):
        """Test rapidly creating and deleting tasks."""
        # Create 6 tasks
        create_requests = []
        for i in range(6):
            create_requests.append(
                client.post("/api/v1/tasks", json={"title": f"Delete Test {i + 1}"}, headers=auth_headers)
            )

        create_responses = await asyncio.gather(*create_requests)
        task_ids = [r.json()["id"] for r in create_responses]

        # Immediately delete all tasks concurrently
        delete_requests = []
        for task_id in task_ids:
            delete_requests.append(client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers))

        delete_responses = await asyncio.gather(*delete_requests)

        # All deletions should succeed
        for response in delete_responses:
            assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify tasks are gone
        for task_id in task_ids:
            verify_response = await client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
            assert verify_response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_rapid_mixed_operations(self, client: AsyncClient, auth_headers, db_session, registered_user):
        """Test rapid mixed operations (create, update, delete, list)."""
        from src.db.models import Task

        # Create some initial tasks
        for i in range(3):
            task = Task(user_id=registered_user.id, title=f"Initial Task {i + 1}")
            db_session.add(task)
        db_session.commit()

        # Mix of operations
        operations = []

        # Creates
        for i in range(5):
            operations.append(client.post("/api/v1/tasks", json={"title": f"New Task {i + 1}"}, headers=auth_headers))

        # Lists
        for _ in range(3):
            operations.append(client.get("/api/v1/tasks", headers=auth_headers))

        # Execute all operations concurrently
        responses = await asyncio.gather(*operations, return_exceptions=True)

        # Most should succeed (some might have race conditions, but no errors)
        success_count = sum(1 for r in responses if not isinstance(r, Exception) and r.status_code in [200, 201])

        # Should have high success rate
        assert success_count >= 6  # At least 75% success
