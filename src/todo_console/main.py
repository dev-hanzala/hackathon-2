import argparse
from todo_console.models import add_task, get_all_tasks, mark_task_complete, update_task, delete_task

def main():
    parser = argparse.ArgumentParser(description="CLI Todo App")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Title of the task")
    add_parser.add_argument("description", type=str, nargs="?", default="", help="Description of the task (optional)")

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as complete")
    complete_parser.add_argument("id", type=int, help="ID of the task to mark complete")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", type=int, help="ID of the task to update")
    update_parser.add_argument("--title", type=str, help="New title for the task")
    update_parser.add_argument("--description", type=str, help="New description for the task")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="ID of the task to delete")

    args = parser.parse_args()

    if args.command == "add":
        task = add_task(args.title, args.description)
        print(f"Task added: ID {task.id}, Title: '{task.title}'")
    elif args.command == "list":
        tasks = get_all_tasks()
        if not tasks:
            print("No tasks found.")
        else:
            for task in tasks:
                print(f"ID: {task.id}, Title: {task.title}, Description: {task.description}, Status: {task.status}")
    elif args.command == "complete":
        task = mark_task_complete(args.id)
        if task:
            print(f"Task {task.id} marked as completed.")
        else:
            print(f"Error: Task with ID {args.id} not found.")
    elif args.command == "update":
        if args.title is None and args.description is None:
            print("Error: No update parameters provided. Use --title or --description.")
        else:
            updated_task = update_task(args.id, args.title, args.description)
            if updated_task:
                print(f"Task {updated_task.id} updated. New Title: '{updated_task.title}', New Description: '{updated_task.description}'")
            else:
                print(f"Error: Task with ID {args.id} not found.")
    elif args.command == "delete":
        deleted_task = delete_task(args.id)
        if deleted_task:
            print(f"Task {deleted_task.id} deleted.")
        else:
            print(f"Error: Task with ID {args.id} not found.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
