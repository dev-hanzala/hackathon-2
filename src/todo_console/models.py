import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

DATA_FILE = Path("tasks.json")

@dataclass
class Task:
    id: int
    title: str
    description: str
    status: str = "pending"

def _load_tasks() -> list[Task]:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return [Task(**task_data) for task_data in data]

def _save_tasks(tasks: list[Task]):
    with open(DATA_FILE, "w") as f:
        json.dump([task.__dict__ for task in tasks], f, indent=4)

TODOS: list[Task] = _load_tasks()
next_id: int = max([task.id for task in TODOS]) + 1 if TODOS else 1

def add_task(title: str, description: str = "") -> Task:
    global next_id
    task = Task(id=next_id, title=title, description=description)
    TODOS.append(task)
    _save_tasks(TODOS)
    next_id += 1
    return task

def get_all_tasks() -> list[Task]:
    return TODOS

def mark_task_complete(task_id: int) -> Optional[Task]:
    for task in TODOS:
        if task.id == task_id:
            task.status = "completed"
            _save_tasks(TODOS)
            return task
    return None

def update_task(task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
    for task in TODOS:
        if task.id == task_id:
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            _save_tasks(TODOS)
            return task
    return None

def delete_task(task_id: int) -> Optional[Task]:
    global TODOS
    for i, task in enumerate(TODOS):
        if task.id == task_id:
            deleted_task = TODOS.pop(i)
            _save_tasks(TODOS)
            return deleted_task
    return None
