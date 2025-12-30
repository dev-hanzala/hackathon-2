import pytest
import sys
import io
from todo_console.main import main
from todo_console import models

@pytest.fixture(autouse=True)
def clear_todos():
    models.TODOS.clear()
    models.next_id = 1

@pytest.fixture
def call_main():
    def _call_main(args):
        old_argv = sys.argv
        old_stdout = sys.stdout
        sys.argv = ["main.py"] + args
        redirected_output = io.StringIO()
        sys.stdout = redirected_output
        try:
            main()
            output = redirected_output.getvalue()
            return output
        finally:
            sys.argv = old_argv
            sys.stdout = old_stdout
    return _call_main

def test_add_command(call_main):
    output = call_main(["add", "Buy groceries", "Milk, bread, eggs"])
    assert "Task added: ID 1, Title: 'Buy groceries'" in output
    assert len(models.TODOS) == 1
    assert models.TODOS[0].title == "Buy groceries"

def test_add_command_no_description(call_main):
    output = call_main(["add", "Read book"])
    assert "Task added: ID 1, Title: 'Read book'" in output
    assert len(models.TODOS) == 1
    assert models.TODOS[0].title == "Read book"

def test_add_command_multiple_tasks(call_main):
    call_main(["add", "Task 1"])
    call_main(["add", "Task 2"])
    assert len(models.TODOS) == 2
    assert models.TODOS[0].title == "Task 1"
    assert models.TODOS[1].title == "Task 2"

def test_list_command_empty(call_main):
    output = call_main(["list"])
    assert "No tasks found." in output

def test_list_command_with_tasks(call_main):
    call_main(["add", "Task Alpha", "Description Alpha"])
    call_main(["add", "Task Beta"])
    output = call_main(["list"])
    assert "ID: 1, Title: Task Alpha, Description: Description Alpha, Status: pending" in output
    assert "ID: 2, Title: Task Beta, Description: , Status: pending" in output

def test_complete_command_existing_task(call_main):
    call_main(["add", "Task to complete"])
    output = call_main(["complete", "1"])
    assert "Task 1 marked as completed." in output
    assert models.TODOS[0].status == "completed"

def test_complete_command_non_existent_task(call_main):
    output = call_main(["complete", "99"])
    assert "Error: Task with ID 99 not found." in output
    assert len(models.TODOS) == 0

def test_update_command_title_only(call_main):
    call_main(["add", "Original Title", "Original Description"])
    output = call_main(["update", "1", "--title", "New Title"])
    assert "Task 1 updated. New Title: 'New Title', New Description: 'Original Description'" in output
    assert models.TODOS[0].title == "New Title"
    assert models.TODOS[0].description == "Original Description"

def test_update_command_description_only(call_main):
    call_main(["add", "Original Title", "Original Description"])
    output = call_main(["update", "1", "--description", "New Description"])
    assert "Task 1 updated. New Title: 'Original Title', New Description: 'New Description'" in output
    assert models.TODOS[0].title == "Original Title"
    assert models.TODOS[0].description == "New Description"

def test_update_command_both_title_and_description(call_main):
    call_main(["add", "Original Title", "Original Description"])
    output = call_main(["update", "1", "--title", "New Title", "--description", "New Description"])
    assert "Task 1 updated. New Title: 'New Title', New Description: 'New Description'" in output
    assert models.TODOS[0].title == "New Title"
    assert models.TODOS[0].description == "New Description"

def test_update_command_non_existent_task(call_main):
    output = call_main(["update", "99", "--title", "Non Existent"])
    assert "Error: Task with ID 99 not found." in output
    assert len(models.TODOS) == 0

def test_update_command_no_parameters(call_main):
    call_main(["add", "Task 1"])
    output = call_main(["update", "1"])
    assert "Error: No update parameters provided. Use --title or --description." in output
    assert models.TODOS[0].title == "Task 1"

def test_delete_command_existing_task(call_main):
    call_main(["add", "Task to delete"])
    output = call_main(["delete", "1"])
    assert "Task 1 deleted." in output
    assert len(models.TODOS) == 0

def test_delete_command_non_existent_task(call_main):
    output = call_main(["delete", "99"])
    assert "Error: Task with ID 99 not found." in output
    assert len(models.TODOS) == 0
