"""
To-Do List Application
A simple command-line task manager with persistent storage.

Author: Namita Sherakhane
"""

import json
import os
from datetime import datetime

DATA_FILE = "tasks.json"
PRIORITIES = ["low", "medium", "high"]


def load_tasks():
    """Load tasks from the JSON file. Returns an empty list if the file doesn't exist."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("Warning: could not read saved tasks. Starting fresh.")
        return []


def save_tasks(tasks):
    """Save the current task list to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def next_id(tasks):
    """Generate the next task ID (max existing ID + 1, or 1 if empty)."""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


def add_task(tasks, description, priority="medium"):
    """Add a new task to the list."""
    priority = priority.lower()
    if priority not in PRIORITIES:
        priority = "medium"

    task = {
        "id": next_id(tasks),
        "description": description.strip(),
        "priority": priority,
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task #{task['id']}: {task['description']}")


def complete_task(tasks, task_id):
    """Mark a task as completed by ID."""
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            print(f"Marked task #{task_id} as completed.")
            return
    print(f"No task found with ID {task_id}.")


def delete_task(tasks, task_id):
    """Remove a task by ID."""
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print(f"Deleted task #{task_id}.")
            return
    print(f"No task found with ID {task_id}.")


def edit_task(tasks, task_id, new_description):
    """Edit the description of an existing task."""
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description.strip()
            save_tasks(tasks)
            print(f"Updated task #{task_id}.")
            return
    print(f"No task found with ID {task_id}.")


def list_tasks(tasks, filter_by="all"):
    """Print tasks to the console, optionally filtered."""
    if filter_by == "active":
        visible = [t for t in tasks if not t["completed"]]
    elif filter_by == "completed":
        visible = [t for t in tasks if t["completed"]]
    else:
        visible = tasks

    if not visible:
        print("No tasks to show.")
        return

    # Sort by priority (high first), then by creation order
    priority_order = {"high": 0, "medium": 1, "low": 2}
    visible = sorted(visible, key=lambda t: priority_order.get(t["priority"], 1))

    print()
    for task in visible:
        status = "[x]" if task["completed"] else "[ ]"
        print(f"{status} #{task['id']:<3} ({task['priority']:<6}) {task['description']}  -- added {task['created_at']}")
    print()

    remaining = len([t for t in tasks if not t["completed"]])
    print(f"{remaining} task(s) remaining.\n")


def print_menu():
    print(
        """
--- To-Do List ---
1. Add task
2. List tasks
3. Complete task
4. Edit task
5. Delete task
6. Clear completed tasks
7. Exit
"""
    )


def main():
    tasks = load_tasks()

    while True:
        print_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            description = input("Task description: ").strip()
            if not description:
                print("Task description can't be empty.")
                continue
            priority = input("Priority (low/medium/high) [medium]: ").strip().lower() or "medium"
            add_task(tasks, description, priority)

        elif choice == "2":
            filter_by = input("Show (all/active/completed) [all]: ").strip().lower() or "all"
            list_tasks(tasks, filter_by)

        elif choice == "3":
            list_tasks(tasks, "active")
            try:
                task_id = int(input("Task ID to complete: ").strip())
                complete_task(tasks, task_id)
            except ValueError:
                print("Please enter a valid task ID.")

        elif choice == "4":
            list_tasks(tasks)
            try:
                task_id = int(input("Task ID to edit: ").strip())
                new_description = input("New description: ").strip()
                if new_description:
                    edit_task(tasks, task_id, new_description)
                else:
                    print("Description can't be empty.")
            except ValueError:
                print("Please enter a valid task ID.")

        elif choice == "5":
            list_tasks(tasks)
            try:
                task_id = int(input("Task ID to delete: ").strip())
                delete_task(tasks, task_id)
            except ValueError:
                print("Please enter a valid task ID.")

        elif choice == "6":
            before = len(tasks)
            tasks = [t for t in tasks if not t["completed"]]
            save_tasks(tasks)
            print(f"Cleared {before - len(tasks)} completed task(s).")

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose a number from 1-7.")


if __name__ == "__main__":
    main()
