import os
import json
import sys
import time
tasks_json_file = "tasks.json"

def show_tasks()->list:
    if not os.path.exists(tasks_json_file):
        return ["No tasks found."]
    with open(tasks_json_file, 'r') as file:
        return json.load(file)

def save_tasks(task:str)->str:
    if not os.path.exists(tasks_json_file):
        with open(tasks_json_file, 'w') as file:
            json.dump([], file)
    get_task_id = create_task_id()
    get_time = created_task_at()
    if os.path.exists(tasks_json_file):
        with open(tasks_json_file, 'r+') as file:
            tasks = json.load(file)
            tasks.append({"ID":get_task_id, "created_at": get_time, "Task":task , "Status":"Not Started"})
            file.seek(0)
            json.dump(tasks, file)

def delete_tasks(task_ID:int)->str:
    if not os.path.exists(tasks_json_file):
        return "No tasks found to delete."
    with open(tasks_json_file, 'r+') as file:
        tasks = json.load(file)
        task_found = False

        for task in tasks:
            if task["ID"] == task_ID:
                task_found = True
                print("Task Found:", task["Task"])
            updated_tasks = [task for task in tasks if task["ID"] != task_ID]
        
        if not task_found:
            return f"Task ID {task_ID} not found to delete"
        
        for index, task in enumerate(updated_tasks,start=1):
            task["ID"] = index
        
        file.seek(0)
        file.truncate()
        json.dump(updated_tasks, file)
    return f"Deleted tast ID:{task_ID} successfully."

def create_task_id()->int:
    if not os.path.exists(tasks_json_file):
        return 1
    with open(tasks_json_file, 'r') as file:
        tasks = json.load(file)
        return len(tasks) + 1 if tasks else 1

def created_task_at()->time:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def Change_status(Task_ID:int, status:str)->str:
    if not os.path.exists(tasks_json_file):
        return "No tasks found to change status."
    if status.upper() not in ["IN_PROGRESS", "COMPLETED"]:
        return "Invalid status. Use 'IN_PROGRESS' or 'COMPLETED'."
    with open(tasks_json_file, 'r+') as file:
        tasks = json.load(file)
        task_found = False
        for task in tasks:
            if task["ID"] == Task_ID:
                if task["Status"].upper() == status.upper():
                    return f"Task ID {Task_ID} is already in '{status.upper()}' status."
                task["Status"] = status.upper()
                task_found = True
                break
        
        if not task_found:
            return f"Task ID {Task_ID} not found."

        file.seek(0)
        file.truncate()
        json.dump(tasks, file)
    return f"Changed status of task ID {Task_ID} to {status}."



def main():
    if len(sys.argv) < 2:
        print("Usage: task_manager <command> [<task>]")
        print("-------------------------------")
        print("""
Commands:
    list         Show all tasks
    add <task>   Add a new task
    delete <task> Delete a task
    Change_status <task_id> <status> Change the status of a task
    """)
        return

    command = sys.argv[1].lower()
    if command not in ["list", "add", "delete", "change_status"]:
        print("Invalid command. Use 'list', 'add', or 'delete'.")
        return

    if command == "list":
        tasks = show_tasks()
        print("\n----------- All Tasks ------------\n")
        for task in tasks:
            print(task, "\n")
        print("--------------- END --------------\n")
    if command == "add":
        if len(sys.argv)<3 or sys.argv[2].lower() == "help":
            print("\n----------- Error: No task provided ------------\n")
            print("Usage: task_manager add <task>")
            print("Please provide a task to add.")
            print("-------------------------------\n")
            return
        description = sys.argv[2]
        save_tasks(description)
        print(f"Task added: {description}")   
    if command == "delete":
        if len(sys.argv)<3 or sys.argv[2].lower() == "help":
            print("Please provide a task to delete.")
            return
        task_ID = int(sys.argv[2])
        print(delete_tasks(task_ID))
    if command == "change_status":
        if len(sys.argv) < 4 or sys.argv[2].lower() == "help":
            print("\n----------- Error: No task ID or status provided ------------\n")
            print("Usage: task_manager Change_status <task_id> <status>")
            print("Please provide a task ID and status to change.")
            print("-------------------------------\n")
            return
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Invalid task ID. Please provide a numeric ID.")
            return
        status = sys.argv[3]
        result = Change_status(task_id, status)
        print("\n----------- Status Change Result ------------\n")
        print(result)
        print("-------------------------------\n")

if __name__ == "__main__":
    main()



        