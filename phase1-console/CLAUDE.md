# Phase I: In-Memory Todo Console App

## Overview

This is the Phase I implementation of the Todo Evolution project - a command-line/TUI todo application with in-memory storage.

**Status:** Completed
**Parent Constitution:** `../.specify/memory/constitution.md`

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Runtime | Python 3.13+ |
| Package Manager | uv |
| TUI Framework | Textual |
| CLI Framework | Click |
| Testing | pytest |
| Linting | ruff |

---

## Commands

```bash
# Navigate to phase1-console directory
cd phase1-console/

# Install dependencies
uv sync

# Run the TUI application
uv run python -m src.todo_console.main

# Run tests
uv run pytest

# Lint code
uv run ruff check .
```

---

## Directory Structure

```
phase1-console/
├── CLAUDE.md           # This file
├── README.md           # Setup and usage instructions
├── pyproject.toml      # Python dependencies
├── .python-version     # Python version (3.13+)
├── src/
│   └── todo_console/
│       ├── __init__.py
│       ├── main.py     # Application entry point
│       ├── models.py   # Task data model
│       └── tui.py      # Textual UI components
└── tests/
    ├── unit/
    │   └── test_models.py
    └── integration/
```

---

## Features (Basic Level)

All 5 Basic Level features are implemented:

1. **Add Task** - Create new todo items with title and description
2. **View Task List** - Display all tasks with ID, title, description, status
3. **Update Task** - Modify existing task details
4. **Delete Task** - Remove tasks by ID
5. **Mark Complete** - Toggle task completion status

---

## Data Model

```python
# In-memory storage (no persistence)
TODOS: list[dict] = []

# Task structure
{
    "id": int,           # Unique identifier
    "title": str,        # Task title (required)
    "description": str,  # Task description (optional)
    "completed": bool    # Completion status
}
```

---

## Constraints (Phase I)

- **No Persistence:** Data lives in Python variables only (no SQL, JSON, files)
- **Single User:** No authentication or multi-user support
- **Single Session:** Data is lost when application exits
- **TUI Interface:** Textual-based interface (no web server)

---

## Keybindings

| Key | Action |
|-----|--------|
| `d` | Toggle dark mode |
| `q` | Quit application |

---

## Related Specs

- Feature Spec: `../specs/001-todo-mvp-cli/spec.md`
- Implementation Plan: `../specs/001-todo-mvp-cli/plan.md`
- Tasks: `../specs/001-todo-mvp-cli/tasks.md`
