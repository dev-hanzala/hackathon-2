# TUI Todo Application

This is a simple Text User Interface (TUI) Todo application built with Python 3.13+ and [Textual](https://textual.io/).
It allows users to manage their tasks by adding, listing, completing, updating, and deleting them within a single session.
Tasks are stored in-memory within the application's runtime and are not persisted to a file.

## Features

- **Add Task**: Add a new task with a title and an optional description using input fields.
- **List Tasks**: View all existing tasks with their ID, title, description, and status in a list view.
- **Complete Task**: Mark a selected task as completed using a button.
- **Update Task**: Modify the title or description of a selected task using input fields and a button.
- **Delete Task**: Remove a selected task from the list using a button.
- **Dark Mode**: Toggle dark mode with `d` keybinding.
- **Quit**: Exit the application with `q` keybinding.

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
    uv pip install -e . textual
    ```

## Usage

To run the application, use the following command:

```bash
uv run python -m src.todo_console.main
```

Once the TUI is running:

-   Use the input fields at the top to add or update task details.
-   Click the "Add Task" button to create a new task.
-   Select a task from the list to enable "Complete", "Update", and "Delete" actions.
-   Click the "Complete Task" button to mark the selected task as completed.
-   Enter new title/description in the input fields and click "Update Task" to modify the selected task.
-   Click the "Delete Task" button to remove the selected task.
-   Press `d` to toggle dark mode.
-   Press `q` to quit the application.

## Testing

To run the unit tests (integration tests were removed as the CLI is replaced by TUI):

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