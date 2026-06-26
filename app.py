"""
To-Do List App (Streamlit version)
A simple web-based task manager with persistent storage.

Author: Namita Sherakhane
"""

import json
import os
from datetime import datetime

import streamlit as st

DATA_FILE = "tasks.json"
PRIORITIES = ["low", "medium", "high"]
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
PRIORITY_COLOR = {"high": "🔴", "medium": "🟠", "low": "🔵"}


# ---------- Data layer ----------

def load_tasks():
    """Load tasks from the JSON file. Returns an empty list if the file doesn't exist."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
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


def add_task(description, priority):
    description = description.strip()
    if not description:
        return
    task = {
        "id": next_id(st.session_state.tasks),
        "description": description,
        "priority": priority,
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    st.session_state.tasks.append(task)
    save_tasks(st.session_state.tasks)


def toggle_task(task_id):
    for task in st.session_state.tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            save_tasks(st.session_state.tasks)
            return


def delete_task(task_id):
    st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task_id]
    save_tasks(st.session_state.tasks)


def clear_completed():
    st.session_state.tasks = [t for t in st.session_state.tasks if not t["completed"]]
    save_tasks(st.session_state.tasks)


# ---------- App setup ----------

st.set_page_config(page_title="To-Do List", page_icon="✅", layout="centered")

if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

st.title("To-Do List")
st.caption(datetime.now().strftime("%A, %B %d"))

# ---------- Add task form ----------

with st.form("add_task_form", clear_on_submit=True):
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        new_task = st.text_input("Task description", placeholder="Add a task", label_visibility="collapsed")
    with col2:
        new_priority = st.selectbox("Priority", PRIORITIES, index=1, label_visibility="collapsed")
    with col3:
        submitted = st.form_submit_button("Add", use_container_width=True)

    if submitted and new_task.strip():
        add_task(new_task, new_priority)
        st.rerun()

st.divider()

# ---------- Filter ----------

filter_choice = st.radio(
    "Filter",
    ["All", "Active", "Completed"],
    horizontal=True,
    label_visibility="collapsed",
)

tasks = st.session_state.tasks

if filter_choice == "Active":
    visible_tasks = [t for t in tasks if not t["completed"]]
elif filter_choice == "Completed":
    visible_tasks = [t for t in tasks if t["completed"]]
else:
    visible_tasks = tasks

visible_tasks = sorted(visible_tasks, key=lambda t: PRIORITY_ORDER.get(t["priority"], 1))

# ---------- Task list ----------

if not visible_tasks:
    st.info("No tasks to show. Add one above to get started.")
else:
    for task in visible_tasks:
        col_check, col_text, col_delete = st.columns([0.5, 5, 0.7])

        with col_check:
            checked = st.checkbox(
                "",
                value=task["completed"],
                key=f"check_{task['id']}",
                label_visibility="collapsed",
            )
            if checked != task["completed"]:
                toggle_task(task["id"])
                st.rerun()

        with col_text:
            label = f"{PRIORITY_COLOR[task['priority']]} {task['description']}"
            if task["completed"]:
                st.markdown(f"~~{label}~~  \n:gray[{task['priority']} · added {task['created_at']}]")
            else:
                st.markdown(f"{label}  \n:gray[{task['priority']} · added {task['created_at']}]")

        with col_delete:
            if st.button("✕", key=f"delete_{task['id']}", help="Delete task"):
                delete_task(task["id"])
                st.rerun()

st.divider()

# ---------- Footer ----------

remaining = len([t for t in tasks if not t["completed"]])
col_count, col_clear = st.columns([3, 1])
with col_count:
    st.caption(f"{remaining} task{'s' if remaining != 1 else ''} left")
with col_clear:
    if st.button("Clear completed", use_container_width=True):
        clear_completed()
        st.rerun()
