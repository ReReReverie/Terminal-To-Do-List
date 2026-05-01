from todo_functions import add_task, view_tasks, finish_task, view_history, delete_task

def main():
    while True:
        print("\n=== To-Do List Menu ===")
        print("1. Add a task")
        print("2. View active tasks")
        print("3. Mark task as finished")
        print("4. View history (Calendar)")
        print("5. Delete a task")
        print("6. Exit")
        
        choice = input("Choose an option (1-6): ")
        
        if choice == '1':
            add_task()
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            finish_task()
        elif choice == '4':
            view_history()
        elif choice == '5':
            delete_task()
        elif choice == '6':
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
