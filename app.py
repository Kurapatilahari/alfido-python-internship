"""
Task 4: Flask Mini Project - Task Manager (Interview Favorite)
------------------------------------------------------------------
Goal: Build a simple web application to demonstrate backend fundamentals.

Features:
    1. Flask routing and Jinja2 templates
    2. Form handling (GET & POST)
    3. Basic CRUD (Create, Read, Update, Delete) using a JSON file as storage
    4. Clean UI using Bootstrap

Author: <Your Name>
"""

import json
import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-in-production"  # needed for flash messages

DATA_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")


# ---------------------------------------------------------
# Simple JSON-file "database" helpers
# ---------------------------------------------------------
def load_tasks():
    """Load all tasks from the JSON storage file. Returns an empty list if none exist."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_tasks(tasks):
    """Persist the tasks list back to the JSON storage file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def get_next_id(tasks):
    """Compute the next available task ID."""
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


# ---------------------------------------------------------
# Routes
# ---------------------------------------------------------
@app.route("/")
def index():
    """READ: display all tasks, with optional status filter via query string (?status=done)."""
    tasks = load_tasks()
    status_filter = request.args.get("status")  # GET query param example
    if status_filter in ("done", "pending"):
        want_done = status_filter == "done"
        tasks = [t for t in tasks if t["done"] == want_done]
    return render_template("index.html", tasks=tasks, status_filter=status_filter)


@app.route("/add", methods=["GET", "POST"])
def add_task():
    """CREATE: show a form (GET) and handle its submission (POST)."""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()

        if not title:
            flash("Title is required.", "danger")
            return redirect(url_for("add_task"))

        tasks = load_tasks()
        new_task = {
            "id": get_next_id(tasks),
            "title": title,
            "description": description,
            "done": False,
        }
        tasks.append(new_task)
        save_tasks(tasks)
        flash(f"Task '{title}' added successfully!", "success")
        return redirect(url_for("index"))

    # GET request -> just show the empty form
    return render_template("add_task.html")


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    """UPDATE: edit an existing task's title/description/status."""
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)

    if task is None:
        flash("Task not found.", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        done = request.form.get("done") == "on"  # checkbox value

        if not title:
            flash("Title is required.", "danger")
            return redirect(url_for("edit_task", task_id=task_id))

        task["title"] = title
        task["description"] = description
        task["done"] = done
        save_tasks(tasks)
        flash(f"Task '{title}' updated.", "success")
        return redirect(url_for("index"))

    return render_template("edit_task.html", task=task)


@app.route("/toggle/<int:task_id>")
def toggle_task(task_id):
    """UPDATE (quick action): toggle a task's done status from the list view."""
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task:
        task["done"] = not task["done"]
        save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    """DELETE: remove a task by ID."""
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    flash("Task deleted.", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    # debug=True is fine for local development / demo purposes only
    app.run(debug=True)
