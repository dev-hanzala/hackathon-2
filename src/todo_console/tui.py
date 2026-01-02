from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, ListView, ListItem, Static, Input, Button
from textual.containers import Container, Horizontal
from todo_console.models import get_all_tasks, add_task, mark_task_complete, update_task, delete_task, TODOS, next_id

class TodoApp(App):
    CSS = """
    Screen:dark {
        background: #202020;
        color: #f0f0f0;
    }
    Screen {
        background: #f0f0f0; /* Default light mode background */
        color: #202020;    /* Default light mode text */
    }
    """
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Label("Welcome to TodoApp TUI!")
        with Container():
            yield ListView(id="task_list") # Moved to top
            yield Input(placeholder="Task Title", id="task_title_input")
            yield Input(placeholder="Task Description (Optional)", id="task_description_input")
            yield Horizontal(
                Button("Add Task", id="add_task_button", variant="primary"),
                Button("Complete Task", id="complete_task_button"),
                Button("Update Task", id="update_task_button"),
                Button("Delete Task", id="delete_task_button", variant="error"),
            )
            yield Label("", id="status_message", classes="hidden")

    def on_mount(self) -> None:
        self.set_dark(False)  # Initialize dark mode to off (light mode)
        TODOS.clear() # Clear tasks for a fresh session
        next_id = 1   # Reset next_id
        self.update_task_list()
        self.query_one("#task_list").focus() # Set initial focus to the task list

    def update_task_list(self) -> None:
        task_list_view = self.query_one("#task_list", ListView)
        task_list_view.clear()
        tasks = get_all_tasks()
        if tasks:
            for task in tasks:
                task_list_view.append(ListItem(Static(f"{task.id}. {task.title} [{task.status}]", classes="task-item")))
        else:
            task_list_view.append(ListItem(Static("No tasks found.")))

    def show_message(self, message: str, is_error: bool = False) -> None:
        status_label = self.query_one("#status_message", Label)
        status_label.update(message)
        status_label.remove_class("hidden")
        status_label.set_class(is_error, "error")
        status_label.set_class(not is_error, "success")

    def get_selected_task_id(self) -> int | None:
        task_list_view = self.query_one("#task_list", ListView)
        if task_list_view.highlighted_child:
            task_item_static = task_list_view.highlighted_child.query_one(".task-item", Static)
            task_id_str = str(task_item_static.render()).split(".")[0]
            return int(task_id_str)
        return None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add_task_button":
            title_input = self.query_one("#task_title_input", Input)
            description_input = self.query_one("#task_description_input", Input)
            title = title_input.value
            description = description_input.value
            if title:
                add_task(title, description)
                title_input.value = ""
                description_input.value = ""
                self.update_task_list()
                self.show_message(f"Task added: '{title}'")
            else:
                self.show_message("Error: Task title cannot be empty.", is_error=True)
        elif event.button.id == "complete_task_button":
            task_id = self.get_selected_task_id()
            if task_id:
                task = mark_task_complete(task_id)
                if task:
                    self.update_task_list()
                    self.show_message(f"Task {task_id} marked as completed.")
                else:
                    self.show_message(f"Error: Task with ID {task_id} not found.", is_error=True)
            else:
                self.show_message("Error: No task selected to complete.", is_error=True)
        elif event.button.id == "update_task_button":
            task_id = self.get_selected_task_id()
            if task_id:
                title_input = self.query_one("#task_title_input", Input)
                description_input = self.query_one("#task_description_input", Input)
                new_title = title_input.value if title_input.value else None
                new_description = description_input.value if description_input.value else None

                if new_title is None and new_description is None:
                    self.show_message("Error: No update parameters provided. Use title or description input fields.", is_error=True)
                else:
                    updated_task = update_task(task_id, new_title, new_description)
                    if updated_task:
                        self.update_task_list()
                        self.show_message(f"Task {task_id} updated.")
                        title_input.value = ""
                        description_input.value = ""
                    else:
                        self.show_message(f"Error: Task with ID {task_id} not found or no changes made.", is_error=True)
            else:
                self.show_message("Error: No task selected to update.", is_error=True)
        elif event.button.id == "delete_task_button":
            task_id = self.get_selected_task_id()
            if task_id:
                deleted_task = delete_task(task_id)
                if deleted_task:
                    self.update_task_list()
                    self.show_message(f"Task {task_id} deleted.")
                else:
                    self.show_message(f"Error: Task with ID {task_id} not found.", is_error=True)
            else:
                self.show_message("Error: No task selected to delete.", is_error=True)

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def action_quit(self) -> None:
        self.exit()