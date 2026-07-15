# Task 4: Flask Mini Project — Task Manager (Interview Favorite)

## Goal
Build a simple web application to demonstrate backend fundamentals.

## Features
- Flask routing and Jinja2 templates
- Form handling for both **GET** and **POST**
- Basic **CRUD** (Create, Read, Update, Delete) — tasks are stored in `tasks.json`
  (no database setup needed, easy to demo)
- Clean, responsive UI using **Bootstrap 5**
- Bonus: filter tasks by status (`All` / `Pending` / `Done`) via query string,
  flash messages for user feedback, and a "toggle done" quick action

## Setup
```bash
pip install -r requirements.txt
```

## How to Run
```bash
python3 app.py
```
Then open your browser to **http://127.0.0.1:5000**

## Project Structure
```
task4_flask_app/
├── app.py                 # Flask routes + CRUD logic
├── requirements.txt
├── tasks.json              # auto-created on first run (acts as the "database")
├── templates/
│   ├── base.html           # shared layout + Bootstrap + navbar
│   ├── index.html          # task list view
│   ├── add_task.html       # create form
│   └── edit_task.html      # edit form
└── static/
    └── style.css            # small custom styling on top of Bootstrap
```

## Routes
| Route | Method | Purpose |
|---|---|---|
| `/` | GET | List all tasks (supports `?status=done` / `?status=pending`) |
| `/add` | GET, POST | Show the "add task" form / handle submission |
| `/edit/<id>` | GET, POST | Show the "edit task" form / handle submission |
| `/toggle/<id>` | GET | Quickly mark a task done/undone |
| `/delete/<id>` | GET | Delete a task |

## Key Concepts Demonstrated
| Concept | Where |
|---|---|
| Routing | `@app.route()` decorators in `app.py` |
| Templates | Jinja2 inheritance (`base.html` + child templates) |
| GET vs POST | `add_task()` and `edit_task()` check `request.method` |
| Form handling | `request.form.get(...)` |
| CRUD | `load_tasks()` / `save_tasks()` + the 5 routes above |
| Clean UI | Bootstrap 5 via CDN, custom `static/style.css` |
