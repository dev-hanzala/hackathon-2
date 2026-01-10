# Phase I: Todo Console Application

A Text User Interface (TUI) Todo application built with Python 3.13+ and [Textual](https://textual.io/). Tasks are stored in-memory and are not persisted to disk.

## Features

- **Add Task**: Add a new task with title and optional description
- **List Tasks**: View all tasks with ID, title, description, and status
- **Complete Task**: Mark a task as completed
- **Update Task**: Modify task title or description
- **Delete Task**: Remove a task from the list
- **Dark Mode**: Toggle with `d` keybinding
- **Quit**: Exit with `q` keybinding

## Installation

```bash
# Navigate to phase1-console directory
cd phase1-console/

# Install uv (if not installed)
pip install uv

# Install dependencies
uv sync
```

## Usage

```bash
# Run the TUI application
uv run python -m src.todo_console.main
```

### TUI Controls

- Use input fields at the top to enter task details
- Click **Add Task** to create a new task
- Select a task from the list to enable actions
- Click **Complete Task** to mark selected task as done
- Click **Update Task** to modify selected task
- Click **Delete Task** to remove selected task
- Press `d` to toggle dark mode
- Press `q` to quit

## Testing

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v
```

## Linting

```bash
# Check for issues
uv run ruff check .

# Auto-fix issues
uv run ruff check . --fix
```

## Project Structure

```
phase1-console/
├── src/
│   └── todo_console/
│       ├── __init__.py     # Package init
│       ├── main.py         # Entry point
│       ├── models.py       # Task model & storage
│       └── tui.py          # Textual UI
├── tests/
│   ├── unit/
│   │   └── test_models.py
│   └── integration/
├── pyproject.toml          # Dependencies
└── README.md               # This file
```

## Constraints

This is Phase I of the Todo Evolution project:

- **In-Memory Only**: No database or file persistence
- **Single Session**: Data is lost when app closes
- **Single User**: No authentication

## Next Phase

Phase II evolves this into a full-stack web application with:
- FastAPI backend
- Next.js frontend
- Neon PostgreSQL database
- Better Auth authentication

See `../backend/` and `../frontend/` for Phase II code.
