import json
from pathlib import Path

DATA_FILE = Path("tasks.json")


def load_tasks():
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        print("Could not load tasks. Starting with an empty list.")
        return []


def save_tasks(tasks):
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4, ensure_ascii=False)

    except OSError:
        print("Could not save tasks.")


def get_next_id(tasks):
    if not tasks:
        return 1

    return max(task["id"] for task in tasks) + 1


def add_task(tasks, title):
    task = {
        "id": get_next_id(tasks),
        "title": title,
        "completed": False,
    }

    tasks.append(task)
    save_tasks(tasks)

    print(f"Task #{task['id']} added.")


def show_tasks(tasks):
    if not tasks:
        print("No tasks.")
        return

    for task in tasks:
        status = "✓" if task["completed"] else " "
        print(f"[{status}] #{task['id']} - {task['title']}")


def complete_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)

            print(f"Task #{task_id} completed.")
            return

    print(f"Task #{task_id} not found.")


def delete_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)

            print(f"Task #{task_id} deleted.")
            return

    print(f"Task #{task_id} not found.")


def main():
    tasks = load_tasks()

    while True:
        print("\nTask Manager")
        print("1. Add task")
        print("2. Show tasks")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            title = input("Task title: ")
            add_task(tasks, title)

        elif choice == "2":
            show_tasks(tasks)

        elif choice == "3":
            try:
                task_id = int(input("Task ID: "))
                complete_task(tasks, task_id)
            except ValueError:
                print("Task ID must be a number.")

        elif choice == "4":
            try:
                task_id = int(input("Task ID: "))
                delete_task(tasks, task_id)
            except ValueError:
                print("Task ID must be a number.")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
