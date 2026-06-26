# To-Do List App

A web-based task manager built with Python and Streamlit. Add, complete, and delete tasks, filter by status, and assign priority levels — all from a clean browser interface. Tasks are saved automatically to a local JSON file, so your list persists between sessions.

**Live app:** [add your Streamlit Cloud link here once deployed]

## Features

- Add tasks with a priority level (low / medium / high)
- Filter tasks by all / active / completed
- Mark tasks as complete with a checkbox
- Delete individual tasks
- Clear all completed tasks at once
- Tasks auto-save to `tasks.json` and reload on the next run

## Tech stack

- Python 3
- [Streamlit](https://streamlit.io/) for the web interface

## Getting started

### Prerequisites

- Python 3.8 or later

### Run it locally

```bash
git clone https://github.com/namitams/todo-list-app.git
cd todo-list-app
pip install -r requirements.txt
streamlit run app.py
```

This opens the app automatically in your browser at `http://localhost:8501`.

## How it works

Tasks are stored as a list of dictionaries (id, description, priority, completed status, and timestamp) and saved to `tasks.json` after every change. Streamlit's `session_state` keeps the task list in memory while the app is open, and the JSON file ensures nothing is lost between runs. Each task gets a unique ID based on the highest existing ID, so IDs stay stable even after deletions.

## Deploying it yourself

This app is built to deploy for free on [Streamlit Community Cloud](https://streamlit.io/cloud):

1. Push this repo to GitHub (already done if you're reading this on GitHub)
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app**, select this repo, and set the main file to `app.py`
4. Click **Deploy** — you'll get a public link like `https://your-app-name.streamlit.app`
5. Add that link to the top of this README and to your resume/LinkedIn

## Possible improvements

- Due dates and reminders
- Search and sort
- Multiple user support
- Exporting tasks to CSV

## Author

Namita Sherakhane
