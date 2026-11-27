import json
import os
import platform
from datetime import datetime

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
def menu():
    while True:
        clear_screen()
        print("\n--- TODO CLI APP MENU ---")
        print("1. Add Task")
        print("2. View Task")
        print("3. Complete Task")
        print("4. Edit Task")
        print("5. Delete Task")
        print("6. Filter Task")
        print("7. Save & Exit")
            
        menu_input = input("\nEnter your choice (1-7): ")
        print("-" * 28) 
    
        if menu_input == "1":
            clear_screen()
            add_task(tasks)
            input("\nPress Enter to return to the menu...")
        elif menu_input == "2":
            view_task(tasks)
            input("\nPress Enter to return to the menu...")
        elif menu_input == "3":
            clear_screen()
            complete_task(tasks)
            input("\nPress Enter to return to the menu...")
        elif menu_input == "4":
            clear_screen()
            edit_task(tasks)
            input("\nPress Enter to return to the menu...")
        elif menu_input == "5":
            clear_screen()
            delete_task(tasks)
            input("\nPress Enter to return to the menu...")
        elif menu_input == "6":
            clear_screen()
            filter_task(tasks)
            input("\nPress Enter to return to the menu...")
        elif menu_input == "7":
            clear_screen()
            save_task(tasks)
            break
        else:
            print("Enter a valid number")
            input("\nPress Enter to return to the menu...")



def load_tasks(): 
    try:
        with open("todo_cli_application.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

tasks = load_tasks()
def save_task(tasks):
    with open("todo_cli_application.json","w") as file:
        json.dump(tasks,file, indent=4)
    print("Data saved successfully.")

def add_task(tasks):
     while True:
        try:      
            while True:
                new_task = input("What is the task? ").strip().lower()
                if new_task != "":
                    break
                else:
                    print("Error: Task cannot be empty ")
            while True:
                category = input("What is the category of the task? ").strip().lower()
                if category != "":
                    break
                else:
                    print("Error: Category cannot be empty ")
            start_date = datetime.now().strftime("%Y-%m-%d %H:%M")
            #date_input = input("What is the date it ended? (YYYY-MM-DD HH:MM): ").strip()
            #parsed_end_date = datetime.strptime(date_input, "%Y-%m-%d %H:%M")
            #end_date = datetime.strftime(parsed_end_date,"%Y-%m-%d %H:%M")
            new_task = {
                "task": new_task,
                "category": category,
                "start_date": start_date,
                "end_date": "",
                "status": "pending",
            }
            tasks.append(new_task)
            print("Task added succesfully")
            return True
        except ValueError:
            print("Error: Invalid date/time format. Please match YYYY-MM-DD HH:MM exactly (e.g., 2026-12-25 18:30).")


def view_task(tasks):

    if not tasks:
        print("\n" + "=" * 60)
        print("                    YOUR TASKS                   ")
        print("=" * 60)
        print("  No tasks found. Your to-do list is empty!")
        print("=" * 60)
        return

    print("\n" + "=" * 60)
    print("                    YOUR TASKS                   ")
    print("=" * 60)

    
    for index, task in enumerate(tasks, start=1):

        status_icon = "✓" if task["status"] == "complete" else "○"
        status_badge = "[COMPLETE]" if task["status"] == "complete" else "[PENDING]"

        print(f"  {index}. {status_icon} {task["task"]}")
        print(f"     Category: {task["category"]:<12} | Status: {status_badge}")
        print(f"     Started:  {task["start_date"]:<12} | Ended:  {task["end_date"]}")
        print("  " + "-" * 56)

    
    completed_count = sum(1 for t in tasks if t.get("status", "").lower() == "complete")
    print(f"  Total: {len(tasks)} | Completed: {completed_count} | Pending: {len(tasks) - completed_count}")
    print("=" * 60)


def complete_task(tasks):
    if not tasks:
        print("No tasks available.")
        return

    
    for index, task in enumerate(tasks, start=1):
        status = task.get("status", "pending")
        print(f"{index}. {task['task']} [{status}]")

    
    try:
        task_to_complete = int(
            input("What task number do you want to complete? ")
        )
    except ValueError:
        print("Enter a valid number")
        return

    
    if not 1 <= task_to_complete <= len(tasks):
        print("Enter a valid task number")
        return

    selected_task = tasks[task_to_complete - 1]

    if selected_task["status"] == "pending":
        selected_task["status"] = "complete"
        selected_task["end_date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        print(f"Task '{selected_task['task']}' marked as complete!")
    else:
        print("Task already completed")

def edit_task(tasks):
    if not tasks:
        print("\n" + "=" * 50)
        print("                EDIT TASK                ")
        print("=" * 50)
        print("  No tasks available to edit.")
        print("=" * 50)
        return

    
    print("\n" + "=" * 50)
    print("                EDIT TASK                ")
    print("=" * 50)

    for index, task in enumerate(tasks, start=1):
        print(f"  {index}. {task["task"]:<25} ({task["category"]}) bat[{task["status"]}]")
        print("-" * 50)
    try:
        task_number = int(input("Enter the task number to edit: ").strip())
    except ValueError:
        print("\n✖ Error: Please: Enter a valid number")
        return

    if not 1 <= task_number <= len(tasks):
        print(f"\n✖ Error: Task #{task_number} does not exist.")
        return

    selected_task = tasks[task_number - 1]
    print("\nSelect the field you want to edit:")
    print("1. Task")
    print("2. Category")
    print("3. Start Date")
    print("4. End Date")

    field_choice = input("\nWhat field do you want to edit? ").strip().lower()
    
    if field_choice == "1":
        selected_task["task"] = input("Enter new task: ").strip()
        field_name = "Task"
        updated_value = selected_task["task"]
    elif field_choice == "2":
        selected_task["category"] = input("Enter new category: ").strip().lower()
        field_name = "Category"
        updated_value = selected_task["category"]
    elif field_choice == "3":
        selected_task["start_date"] = input("Enter new start_date (YYYY-MM-DD HH:MM): ")
        field_name = "start_date"
        updated_value = selected_task["start_date"]
    elif field_choice == "4":
        selected_task["end_date"] = input("Enter new end_date (YYYY-MM-DD HH:MM): ")
        field_name = "end_date"
        updated_value = selected_task["end_date"]
    else:
        print("\n✖ Invalid field choice. Choose from: task, category, start date, or end date.")
        return
    print("\n" + "-" * 50)
    print(f"✔ Field '{field_name}' updated successfully to: '{updated_value}'")
    print("-" * 50)
#edit_task(tasks)

def delete_task(tasks):
    if not tasks:
        print("\n=== Delete Task ===")
        print("No tasks available to delete.")
        return

    print("\n" + "=" * 40)
    print("               DELETE TASK              ")
    print("=" * 40)

    for index, task in enumerate(tasks, start=1):

        status_icon = "✓" if task["status"] == "complete" else "○"

        print(f"  {index}. [{status_icon}] {task.get("task"):<25} ({task["category"]}) [{task["status"].upper()}]")

    print("-" * 40)

    
    try:
        task_to_delete = int(input("Enter the task number to delete: ").strip())
    except ValueError:
        print("\n✖ Error: Please enter a valid number.")
        return

    if not 1 <= task_to_delete <= len(tasks):
        print(f"\n✖ Error: Task #{task_to_delete} does not exist.")
        return

    deleted_task = tasks.pop(task_to_delete - 1)

    print("\n" + "-" * 40)
    print(f"✔ Task '{deleted_task["category"]}' was successfully deleted.")
    print(f"  Remaining tasks in list: {len(tasks)}")
    print("-" * 40)

#delete_task(tasks)
def filter_task(tasks):
    filter_input = (
        input("Filter either by complete or pending status: ").strip().lower()
    )

    if filter_input not in ["complete", "pending"]:
        print("Invalid filter option. Please enter 'complete' or 'pending'.")
        return

    found = False

    for task in tasks:
        if task["status"] == filter_input:
            print(f"- [{task["category"]}] {task["task"]} ({task["status"]})")
            found = True
    if not found:
        print(f"No tasks found with status '{filter_input}'.")


menu()

