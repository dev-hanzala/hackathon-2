from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    description: str
    status: str = "pending"

TODOS: list[Task] = []
next_id: int = 1

def add_task(title: str, description: str = "") -> Task:
    global next_id
    task = Task(id=next_id, title=title, description=description)
    TODOS.append(task)
    next_id += 1
    return task

def get_all_tasks() -> list[Task]:
    return TODOS

def mark_task_complete(task_id: int) -> Optional[Task]:
    for task in TODOS:
        if task.id == task_id:
            task.status = "completed"
            return task
    return None

def update_task(task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
    for task in TODOS:
        if task.id == task_id:
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            return task
    return None

def delete_task(task_id: int) -> Optional[Task]:
    global TODOS
    for i, task in enumerate(TODOS):
        if task.id == task_id:
            return TODOS.pop(i)
    return None
