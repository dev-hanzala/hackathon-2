import pytest
from todo_console import models

@pytest.fixture(autouse=True)
def clear_todos():
    models.TODOS.clear()
    models.next_id = 1

def test_add_task():
    task = models.add_task("Buy groceries", "Milk, bread, eggs")
    assert len(models.TODOS) == 1
    assert task.id == 1
    assert task.title == "Buy groceries"
    assert task.description == "Milk, bread, eggs"
    assert task.status == "pending"
    assert models.next_id == 2

def test_add_task_no_description():
    task = models.add_task("Read book")
    assert len(models.TODOS) == 1
    assert task.id == 1
    assert task.title == "Read book"
    assert task.description == ""
    assert task.status == "pending"
    assert models.next_id == 2

def test_add_multiple_tasks():
    models.add_task("Task 1")
    models.add_task("Task 2")
    assert len(models.TODOS) == 2
    assert models.TODOS[0].id == 1
    assert models.TODOS[1].id == 2
    assert models.next_id == 3

def test_get_all_tasks_empty():
    tasks = models.get_all_tasks()
    assert len(tasks) == 0

def test_get_all_tasks_with_tasks():
    models.add_task("Task A")
    models.add_task("Task B")
    tasks = models.get_all_tasks()
    assert len(tasks) == 2
    assert tasks[0].title == "Task A"
    assert tasks[1].title == "Task B"

def test_mark_task_complete_existing_task():
    task1 = models.add_task("Task 1")
    models.add_task("Task 2") # Ensure there's another task to check length after deletion.
    completed_task = models.mark_task_complete(task1.id)
    assert completed_task is not None
    assert completed_task.id == task1.id
    assert completed_task.status == "completed"
    assert models.TODOS[0].status == "completed"
    assert models.TODOS[1].status == "pending"

def test_mark_task_complete_non_existent_task():
    models.add_task("Task 1")
    completed_task = models.mark_task_complete(99)
    assert completed_task is None
    assert models.TODOS[0].status == "pending"

def test_mark_task_complete_already_completed():
    task1 = models.add_task("Task 1")
    models.mark_task_complete(task1.id)
    completed_task = models.mark_task_complete(task1.id)
    assert completed_task is not None
    assert completed_task.status == "completed"
    assert models.TODOS[0].status == "completed"

def test_update_task_title_only():
    task = models.add_task("Original Title", "Original Description")
    updated_task = models.update_task(task.id, title="New Title")
    assert updated_task is not None
    assert updated_task.title == "New Title"
    assert updated_task.description == "Original Description"

def test_update_task_description_only():
    task = models.add_task("Original Title", "Original Description")
    updated_task = models.update_task(task.id, description="New Description")
    assert updated_task is not None
    assert updated_task.title == "Original Title"
    assert updated_task.description == "New Description"

def test_update_task_both_title_and_description():
    task = models.add_task("Original Title", "Original Description")
    updated_task = models.update_task(task.id, title="New Title", description="New Description")
    assert updated_task is not None
    assert updated_task.title == "New Title"
    assert updated_task.description == "New Description"

def test_update_task_non_existent():
    models.add_task("Task 1")
    updated_task = models.update_task(99, title="Non Existent")
    assert updated_task is None

def test_delete_task_existing_task():
    task1 = models.add_task("Task 1")
    models.add_task("Task 2") # Ensure there's another task to check length after deletion.
    deleted_task = models.delete_task(task1.id)
    assert deleted_task is not None
    assert deleted_task.id == task1.id
    assert len(models.TODOS) == 1
    assert models.TODOS[0].title == "Task 2"

def test_delete_task_non_existent_task():
    models.add_task("Task 1")
    deleted_task = models.delete_task(99)
    assert deleted_task is None
    assert len(models.TODOS) == 1
