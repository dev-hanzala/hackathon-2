"""Integration tests for load performance with 100+ tasks.

T158: Test load performance
- Verify <2 second load time per SC-002
- Test with 100+ tasks
"""

import asyncio
import time

import pytest
from fastapi import status
from httpx import AsyncClient

from src.db.models import Task


class TestLoadPerformance:
    """T158: Integration tests for load performance with 100+ tasks."""

    @pytest.mark.asyncio
    async def test_list_100_tasks_performance(self, client: AsyncClient, auth_headers, db_session, registered_user):
        """Test that listing 100 tasks completes in under 2 seconds (SC-002)."""
        # Create 100 tasks in the database
        tasks = []
        for i in range(100):
            task = Task(
                user_id=registered_user.id,
                title=f"Performance Test Task {i + 1}",
                description=f"Task for performance testing {i + 1}",
                completed=i % 2 == 0,  # Mix of completed and incomplete
            )
            tasks.append(task)

        db_session.add_all(tasks)
        db_session.commit()

        # Measure time to list all tasks
        start_time = time.time()
        response = await client.get("/api/v1/tasks?completed=all&is_archived=all", headers=auth_headers)
        end_time = time.time()

        elapsed_time = end_time - start_time

        # Assertions
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 100

        # SC-002: Should complete in under 2 seconds
        assert elapsed_time < 2.0, f"List operation took {elapsed_time:.2f}s, expected <2s"

    @pytest.mark.asyncio
    async def test_list_200_tasks_performance(self, client: AsyncClient, auth_headers, db_session, registered_user):
        """Test that listing 200 tasks still maintains reasonable performance."""
        # Create 200 tasks in the database
        tasks = []
        for i in range(200):
            task = Task(
                user_id=registered_user.id,
                title=f"Load Test Task {i + 1}",
                description=f"Description {i + 1}",
                completed=i % 3 == 0,
                is_archived=i % 10 == 0,
            )
            tasks.append(task)

        db_session.add_all(tasks)
        db_session.commit()

        # Measure time to list all tasks
        start_time = time.time()
        response = await client.get("/api/v1/tasks?completed=all&is_archived=all", headers=auth_headers)
        end_time = time.time()

        elapsed_time = end_time - start_time

        # Assertions
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 200

        # Should still be reasonably fast (allow 3s for 200 tasks)
        assert elapsed_time < 3.0, f"List operation took {elapsed_time:.2f}s, expected <3s"

    @pytest.mark.asyncio
    async def test_filtered_list_performance_with_100_tasks(
        self, client: AsyncClient, auth_headers, db_session, registered_user
    ):
        """Test that filtered list queries are efficient with 100+ tasks."""
        # Create 150 tasks with mix of completed/incomplete
        tasks = []
        for i in range(150):
            task = Task(
                user_id=registered_user.id,
                title=f"Filter Test Task {i + 1}",
                completed=i % 2 == 0,  # 75 completed, 75 incomplete
            )
            tasks.append(task)

        db_session.add_all(tasks)
        db_session.commit()

        # Test filtering for incomplete tasks (should use index)
        start_time = time.time()
        response = await client.get("/api/v1/tasks?completed=false", headers=auth_headers)
        end_time = time.time()

        elapsed_time = end_time - start_time

        # Assertions
        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Verify filtering worked
        incomplete_tasks = [t for t in data if not t["completed"]]
        assert len(incomplete_tasks) >= 70  # Should have ~75

        # Should be fast due to composite index
        assert elapsed_time < 1.5, f"Filtered list took {elapsed_time:.2f}s, expected <1.5s"

    @pytest.mark.asyncio
    async def test_concurrent_list_requests_with_100_tasks(
        self, client: AsyncClient, auth_headers, db_session, registered_user
    ):
        """Test that multiple concurrent list requests handle load well."""
        # Create 100 tasks
        tasks = []
        for i in range(100):
            task = Task(user_id=registered_user.id, title=f"Concurrent Load Test {i + 1}")
            tasks.append(task)

        db_session.add_all(tasks)
        db_session.commit()

        # Make 10 concurrent list requests
        start_time = time.time()
        requests = []
        for _ in range(10):
            requests.append(client.get("/api/v1/tasks", headers=auth_headers))

        responses = await asyncio.gather(*requests)
        end_time = time.time()

        elapsed_time = end_time - start_time

        # All should succeed
        for response in responses:
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert len(data) >= 100

        # 10 concurrent requests should complete reasonably fast
        assert elapsed_time < 5.0, f"10 concurrent requests took {elapsed_time:.2f}s, expected <5s"

    @pytest.mark.asyncio
    async def test_individual_task_retrieval_performance(
        self, client: AsyncClient, auth_headers, db_session, registered_user
    ):
        """Test that individual task retrieval is fast even with many tasks."""
        # Create 100 tasks
        tasks = []
        for i in range(100):
            task = Task(user_id=registered_user.id, title=f"Retrieval Test {i + 1}")
            tasks.append(task)

        db_session.add_all(tasks)
        db_session.commit()
        db_session.refresh(tasks[0])

        # Retrieve a single task (should use primary key index)
        start_time = time.time()
        response = await client.get(f"/api/v1/tasks/{tasks[0].id}", headers=auth_headers)
        end_time = time.time()

        elapsed_time = end_time - start_time

        # Assertions
        assert response.status_code == status.HTTP_200_OK

        # Should be very fast (single row lookup by PK)
        assert elapsed_time < 0.5, f"Single task retrieval took {elapsed_time:.2f}s, expected <0.5s"

    @pytest.mark.asyncio
    async def test_task_update_performance_with_large_dataset(
        self, client: AsyncClient, auth_headers, db_session, registered_user
    ):
        """Test that task updates are fast even with 100+ tasks in database."""
        # Create 100 tasks
        tasks = []
        for i in range(100):
            task = Task(user_id=registered_user.id, title=f"Update Perf Test {i + 1}")
            tasks.append(task)

        db_session.add_all(tasks)
        db_session.commit()
        db_session.refresh(tasks[50])

        # Update a single task
        start_time = time.time()
        response = await client.put(
            f"/api/v1/tasks/{tasks[50].id}", json={"title": "Updated Title", "completed": True}, headers=auth_headers
        )
        end_time = time.time()

        elapsed_time = end_time - start_time

        # Assertions
        assert response.status_code == status.HTTP_200_OK

        # Should be fast
        assert elapsed_time < 1.0, f"Task update took {elapsed_time:.2f}s, expected <1s"


class TestScalabilityLimits:
    """Tests to verify scalability with even larger datasets."""

    @pytest.mark.asyncio
    async def test_list_500_tasks_scalability(self, client: AsyncClient, auth_headers, db_session, registered_user):
        """Test that the system can handle 500 tasks (stress test)."""
        # Create 500 tasks (batch insert)
        tasks = []
        for i in range(500):
            task = Task(user_id=registered_user.id, title=f"Scalability Test {i + 1}", completed=i % 5 == 0)
            tasks.append(task)

        db_session.add_all(tasks)
        db_session.commit()

        # Measure list performance
        start_time = time.time()
        response = await client.get("/api/v1/tasks?completed=all&is_archived=all", headers=auth_headers)
        end_time = time.time()

        elapsed_time = end_time - start_time

        # Assertions
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 500

        # Should complete in reasonable time (allow 5s for 500 tasks)
        assert elapsed_time < 5.0, f"List 500 tasks took {elapsed_time:.2f}s, expected <5s"

    @pytest.mark.asyncio
    async def test_pagination_performance_hint(self, client: AsyncClient, auth_headers, db_session, registered_user):
        """Test list performance and document that pagination should be considered."""
        # Create 300 tasks
        tasks = []
        for i in range(300):
            task = Task(user_id=registered_user.id, title=f"Pagination Test {i + 1}")
            tasks.append(task)

        db_session.add_all(tasks)
        db_session.commit()

        # List all tasks
        start_time = time.time()
        response = await client.get("/api/v1/tasks", headers=auth_headers)
        end_time = time.time()

        elapsed_time = end_time - start_time

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Document performance characteristics
        # Note: For production with 1000+ tasks, pagination is recommended
        # Current implementation loads all tasks, which works for SC-002
        # but may need optimization for larger datasets

        print(f"\nPerformance note: Listed {len(data)} tasks in {elapsed_time:.3f}s")
        print("For production with >1000 tasks, consider implementing pagination")

    @pytest.mark.asyncio
    async def test_database_index_effectiveness(self, client: AsyncClient, auth_headers, db_session, registered_user):
        """Test that database indexes improve query performance."""
        # Create 200 tasks with specific patterns for index testing
        tasks = []
        for i in range(200):
            task = Task(
                user_id=registered_user.id,
                title=f"Index Test {i + 1}",
                completed=i < 100,  # First 100 completed
                is_archived=i < 50,  # First 50 archived
            )
            tasks.append(task)

        db_session.add_all(tasks)
        db_session.commit()

        # Query using indexed columns (user_id, completed, is_archived)
        # This should use the composite index
        start_time = time.time()
        response = await client.get("/api/v1/tasks?completed=true&is_archived=false", headers=auth_headers)
        end_time = time.time()

        elapsed_time = end_time - start_time

        assert response.status_code == status.HTTP_200_OK

        # Should be very fast due to composite index
        # (user_id, completed, is_archived)
        assert elapsed_time < 1.0, f"Indexed query took {elapsed_time:.2f}s, expected <1s"
