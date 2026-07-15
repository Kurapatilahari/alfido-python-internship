# Task 1: Python File Handling & Automation

## Goal
Understand Python file handling, automation logic, and exception handling.

## What This Script Does
- Reads and writes `.txt` and `.csv` files
- Automates file operations: **rename**, **move**, **delete**
- Uses `try / except` blocks throughout for robust error handling
- Logs every action with a timestamp to `workspace/activity_log.txt`

## How to Run
```bash
python3 file_automation.py
```

A `workspace/` folder will be created automatically (git-ignored) containing:
- `notes.txt` → renamed to `notes_final.txt` → moved into `workspace/archive/`
- `interns.csv` → read, printed, then deleted
- `activity_log.txt` → timestamped log of every operation

## Sample Output
```
============================================================
TASK 1: PYTHON FILE HANDLING & AUTOMATION
============================================================
[OK] Workspace ready at 'workspace/'
[OK] Wrote text file: workspace/notes.txt
[OK] Read text file: workspace/notes.txt

--- notes.txt content ---
This is a demo text file.
Created by file_automation.py

[OK] Wrote CSV file: workspace/interns.csv

--- interns.csv content ---
    -> {'name': 'Alice', 'age': '23', 'role': 'Intern'}
    -> {'name': 'Bob', 'age': '25', 'role': 'Intern'}
    -> {'name': 'Charlie', 'age': '22', 'role': 'Intern'}
[OK] Read CSV file: workspace/interns.csv (3 rows)
[OK] Renamed 'notes.txt' -> 'notes_final.txt'
[OK] Moved 'notes_final.txt' to archive/
[ERROR] Cannot delete, file not found: workspace/does_not_exist.txt
[OK] Deleted: workspace/interns.csv

[DONE] All operations completed. See workspace/activity_log.txt for the full log.
```

## Key Concepts Demonstrated
| Concept | Where |
|---|---|
| Writing files | `write_text_file()`, `write_csv_file()` |
| Reading files | `read_text_file()`, `read_csv_file()` |
| Renaming | `rename_file()` using `os.rename()` |
| Moving | `move_file_to_archive()` using `shutil.move()` |
| Deleting | `delete_file()` using `os.remove()` |
| Exception handling | `try/except` around every file operation (`FileNotFoundError`, `PermissionError`, `IOError`, etc.) |
| Logging/automation | `log_action()` appends timestamped entries |
