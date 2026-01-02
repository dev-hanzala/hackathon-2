# CLI Todo Application

This is a simple Command Line Interface (CLI) Todo application built with Python 3.13+.
It allows users to manage their tasks by adding, listing, completing, updating, and deleting them.
Tasks are stored in-memory within the application's runtime.

## Features

- **Add Task**: Add a new task with a title and an optional description.
- **List Tasks**: View all existing tasks with their ID, title, description, and status.
- **Complete Task**: Mark a task as completed using its ID.
- **Update Task**: Modify the title or description of an existing task by its ID.
- **Delete Task**: Remove a task from the list using its ID.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install `uv` (if you don't have it):**
    ```bash
    pip install uv
    ```

3.  **Install dependencies:**
    ```bash
    uv pip install -e .
    ```

## Usage

To run the application, use the following command:

```bash
uv run python -m src.todo_console.main
```

### Commands

-   **Add a task:**
    ```bash
    uv run python -m src.todo_console.main add "Buy groceries" "Milk, bread, eggs"
    uv run python -m src.todo_console.main add "Read a book"
    ```

-   **List all tasks:**
    ```bash
    uv run python -m src.todo_console.main list
    ```

-   **Complete a task:**
    ```bash
    uv run python -m src.todo_console.main complete 1
    ```
    (Replace `1` with the actual task ID)

-   **Update a task:**
    ```bash
    uv run python -m src.todo_console.main update 1 --title "Buy fruits"
    uv run python -m src.todo_console.main update 2 --description "Read 'The Hitchhiker's Guide to the Galaxy'"
    uv run python -m src.todo_console.main update 1 --title "Buy veggies" --description "Carrots, potatoes"
    ```
    (Replace `1` or `2` with the actual task ID)

-   **Delete a task:**
    ```bash
    uv run python -m src.todo_console.main delete 1
    ```
    (Replace `1` with the actual task ID)

## Testing

To run the unit and integration tests:

```bash
uv run pytest
```

## Linting and Formatting

To check for linting and formatting issues:

```bash
uv run ruff check .
```

To automatically fix linting and formatting issues:

```bash
uv run ruff check . --fix
```