"""
Task 1: Python File Handling & Automation
-------------------------------------------
Goal: Understand Python file handling, automation logic, and exception handling.

This script demonstrates:
    1. Reading and writing files (txt/csv)
    2. Automating file operations (rename, move, delete)
    3. Using try-except for robust error handling
    4. Clear comments explaining the logic

Author: <Your Name>
"""

import os
import csv
import shutil
from datetime import datetime

# ---------------------------------------------------------
# Folder setup - all demo files live inside "workspace/"
# so the script never touches unrelated files on disk.
# ---------------------------------------------------------
WORKSPACE = "workspace"
ARCHIVE = os.path.join(WORKSPACE, "archive")


def setup_workspace():
    """Create the workspace and archive folders if they don't already exist."""
    try:
        os.makedirs(WORKSPACE, exist_ok=True)
        os.makedirs(ARCHIVE, exist_ok=True)
        print(f"[OK] Workspace ready at '{WORKSPACE}/'")
    except OSError as e:
        # Catches permission errors, invalid paths, etc.
        print(f"[ERROR] Could not create workspace folders: {e}")


def write_text_file(filename, content):
    """Write a plain text (.txt) file. Overwrites if it already exists."""
    path = os.path.join(WORKSPACE, filename)
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] Wrote text file: {path}")
    except IOError as e:
        print(f"[ERROR] Failed to write '{path}': {e}")


def read_text_file(filename):
    """Read and return the contents of a text file, handling missing files gracefully."""
    path = os.path.join(WORKSPACE, filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = f.read()
        print(f"[OK] Read text file: {path}")
        return data
    except FileNotFoundError:
        print(f"[ERROR] File not found: {path}")
        return None


def write_csv_file(filename, rows):
    """
    Write a list of dictionaries to a CSV file.
    'rows' is expected to be a list like:
        [{"name": "Alice", "age": 23}, {"name": "Bob", "age": 30}]
    """
    path = os.path.join(WORKSPACE, filename)
    if not rows:
        print("[WARN] No rows provided; skipping CSV write.")
        return
    try:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        print(f"[OK] Wrote CSV file: {path}")
    except (IOError, csv.Error) as e:
        print(f"[ERROR] Failed to write CSV '{path}': {e}")


def read_csv_file(filename):
    """Read a CSV file and print each row. Returns the rows as a list of dicts."""
    path = os.path.join(WORKSPACE, filename)
    rows = []
    try:
        with open(path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
                print(f"    -> {row}")
        print(f"[OK] Read CSV file: {path} ({len(rows)} rows)")
    except FileNotFoundError:
        print(f"[ERROR] File not found: {path}")
    return rows


def rename_file(old_name, new_name):
    """Rename a file inside the workspace folder."""
    old_path = os.path.join(WORKSPACE, old_name)
    new_path = os.path.join(WORKSPACE, new_name)
    try:
        os.rename(old_path, new_path)
        print(f"[OK] Renamed '{old_name}' -> '{new_name}'")
    except FileNotFoundError:
        print(f"[ERROR] Cannot rename, file not found: {old_path}")
    except FileExistsError:
        print(f"[ERROR] A file named '{new_name}' already exists.")


def move_file_to_archive(filename):
    """Move a file from the workspace into the archive subfolder."""
    src = os.path.join(WORKSPACE, filename)
    dst = os.path.join(ARCHIVE, filename)
    try:
        shutil.move(src, dst)
        print(f"[OK] Moved '{filename}' to archive/")
    except FileNotFoundError:
        print(f"[ERROR] Cannot move, file not found: {src}")
    except shutil.Error as e:
        print(f"[ERROR] Move failed: {e}")


def delete_file(filename, in_archive=False):
    """Delete a file, either from the workspace or the archive folder."""
    folder = ARCHIVE if in_archive else WORKSPACE
    path = os.path.join(folder, filename)
    try:
        os.remove(path)
        print(f"[OK] Deleted: {path}")
    except FileNotFoundError:
        print(f"[ERROR] Cannot delete, file not found: {path}")
    except PermissionError:
        print(f"[ERROR] Permission denied while deleting: {path}")


def log_action(message):
    """Append a timestamped log entry to activity_log.txt (demonstrates 'append' mode)."""
    path = os.path.join(WORKSPACE, "activity_log.txt")
    try:
        with open(path, "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {message}\n")
    except IOError as e:
        print(f"[ERROR] Could not write to log: {e}")


def main():
    print("=" * 60)
    print("TASK 1: PYTHON FILE HANDLING & AUTOMATION")
    print("=" * 60)

    # 1. Setup
    setup_workspace()
    log_action("Workspace initialized")

    # 2. Write & read a text file
    write_text_file("notes.txt", "This is a demo text file.\nCreated by file_automation.py\n")
    log_action("Created notes.txt")
    content = read_text_file("notes.txt")
    print("\n--- notes.txt content ---")
    print(content)

    # 3. Write & read a CSV file
    sample_data = [
        {"name": "Alice", "age": "23", "role": "Intern"},
        {"name": "Bob", "age": "25", "role": "Intern"},
        {"name": "Charlie", "age": "22", "role": "Intern"},
    ]
    write_csv_file("interns.csv", sample_data)
    log_action("Created interns.csv")
    print("\n--- interns.csv content ---")
    read_csv_file("interns.csv")

    # 4. Automate file operations: rename -> move -> delete
    rename_file("notes.txt", "notes_final.txt")
    log_action("Renamed notes.txt to notes_final.txt")

    move_file_to_archive("notes_final.txt")
    log_action("Moved notes_final.txt to archive/")

    # Try deleting a file that does NOT exist, to demonstrate error handling
    delete_file("does_not_exist.txt")

    # Delete the CSV to clean up (demonstrates real deletion)
    delete_file("interns.csv")
    log_action("Deleted interns.csv")

    print("\n[DONE] All operations completed. See workspace/activity_log.txt for the full log.")


if __name__ == "__main__":
    main()
