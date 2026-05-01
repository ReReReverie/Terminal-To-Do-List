import json
import os
import datetime

TODOS_FILE = os.path.join(os.path.dirname(__file__), 'data', 'todos.json')
HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'data', 'history.json')

def load_data(filename):
    """Load JSON data from a file, returning an empty list if file doesn't exist or is empty."""
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(filename, data):
    """Save data to a JSON file, ensuring directory exists."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def add_task():
    """Prompt the user for a task and save it to both active and history files."""
    task = input("Enter task description: ")
    todos = load_data(TODOS_FILE)
    history = load_data(HISTORY_FILE)
    
    # Generate an ID based on the highest existing ID in history
    if not history:
        task_id = 1
    else:
        task_id = max(t.get('id', 0) for t in history) + 1
        
    new_task = {
        "id": task_id,
        "task": task,
        "finished": 0,  # 0 indicates not done
        "added_at": datetime.datetime.now().isoformat()
    }
    
    # Add to active tasks
    todos.append(new_task)
    save_data(TODOS_FILE, todos)
    
    # Add to history (history contains both finished and unfinished)
    history.append(new_task)
    save_data(HISTORY_FILE, history)
    
    print(f"Task '{task}' added successfully with ID {task_id}.")

def view_tasks():
    """View all active tasks."""
    todos = load_data(TODOS_FILE)
    if not todos:
        print("No active tasks.")
        return
    print("\n--- Active Tasks ---")
    for t in todos:
        print(f"[{t['id']}] {t['task']}")
    print("--------------------")

def finish_task():
    """Mark an active task as finished (1) and update the history file."""
    view_tasks()
    todos = load_data(TODOS_FILE)
    if not todos:
        return
    
    try:
        task_id = int(input("Enter task ID to mark as finished: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    # Find the task by ID in active tasks
    task_to_finish = next((t for t in todos if t['id'] == task_id), None)
    
    if task_to_finish:
        # Remove from active tasks
        todos.remove(task_to_finish)
        save_data(TODOS_FILE, todos)

        # Update status in history file
        history = load_data(HISTORY_FILE)
        for h_task in history:
            if h_task['id'] == task_id:
                h_task['finished'] = 1  # 1 indicates done
                h_task['finished_at'] = datetime.datetime.now().isoformat()
                break
        
        save_data(HISTORY_FILE, history)
        print(f"Task {task_id} marked as finished (1).")
    else:
        print(f"Task with ID {task_id} not found in active tasks.")

def view_history():
    """View all tasks in the history file, grouped by date."""
    history = load_data(HISTORY_FILE)
    if not history:
        print("History is empty.")
        return
        
    # Group tasks by date
    grouped_tasks = {}
    for t in history:
        added_at_str = t.get('added_at', '')
        if added_at_str:
            try:
                dt = datetime.datetime.fromisoformat(added_at_str)
                date_key = dt.strftime('%Y-%m-%d')
                time_str = dt.strftime('%H:%M:%S')
            except ValueError:
                date_key = "Unknown Date"
                time_str = "Unknown Time"
        else:
            date_key = "Unknown Date"
            time_str = "Unknown Time"
            
        if date_key not in grouped_tasks:
            grouped_tasks[date_key] = []
            
        grouped_tasks[date_key].append((t, time_str))
        
    print("\n--- Task History (Calendar View) ---")
    
    # Sort dates
    sorted_dates = sorted(grouped_tasks.keys())
    
    for date_key in sorted_dates:
        print(f"\n📅 {date_key}:")
        for t, time_str in grouped_tasks[date_key]:
            status_code = t.get('finished', 0)
            status_text = "Done" if status_code == 1 else "Not Done"
            
            finished_str = ""
            if status_code == 1 and t.get('finished_at'):
                try:
                    f_dt = datetime.datetime.fromisoformat(t.get('finished_at'))
                    finished_str = f" - Finished at: {f_dt.strftime('%H:%M:%S')}"
                except ValueError:
                    pass
                    
            print(f"  [{t['id']}] {t['task']} (Created at: {time_str}) - Status: {status_code} ({status_text}){finished_str}")
            
    print("------------------------------------")

def delete_task():
    """Delete a task only from active tasks, keeping it in history."""
    view_tasks()
    todos = load_data(TODOS_FILE)
    
    if not todos:
        print("No active tasks available to delete.")
        return
        
    try:
        task_id = int(input("\nEnter task ID to delete from active tasks: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return
        
    # Remove from active tasks
    task_in_todos = next((t for t in todos if t['id'] == task_id), None)
    if task_in_todos:
        todos.remove(task_in_todos)
        save_data(TODOS_FILE, todos)
        print(f"Task {task_id} successfully deleted from active tasks. (Still available in history)")
    else:
        print(f"Task with ID {task_id} not found in active tasks.")
