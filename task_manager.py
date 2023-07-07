#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

#====Login Section====
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

# Function to register a new user
def reg_user():
    new_username = input("New Username: ")
    if new_username in username_password.keys():
        print("Username already exists. Please choose a different username.")
        return
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")
    if new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))
    else:
        print("Passwords do not match")

# Function to add a new task
def add_task():
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")
    curr_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

# Function to view all tasks
def view_all():
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

# Function to see curr_user tasks
def view_mine():
    task_count = len(task_list)
    if task_count == 0:
        print("No tasks found.")
        return

    print("Tasks assigned to you:")
    for i, task in enumerate(task_list, start=0):
        if task['username'] == curr_user:
            print(f"Task {i}:")
            print(f"Title: {task['title']}")
            print(f"Description: {task['description']}")
            print(f"Due Date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
            print(f"Assigned Date: {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
            print(f"Completed: {'Yes' if task['completed'] else 'No'}")
            print()
    # prompt user for the number of the task to select or allow him to return to the main menu by pressing -1 as requested
    while True:
        task_num = input("Enter the number of the task you want to select (or -1 to return to the main menu): ")
        if task_num == "-1":
            break
        elif not task_num.isdigit() or int(task_num) < 1 or int(task_num) > task_count:
            print("Invalid task number. Please try again.")
            continue

        task_index = int(task_num) - 1
        selected_task = task_list[task_index]
        if selected_task['completed']:
            print("Task is already completed. You cannot edit it.")
            continue

        print(f"Task {task_num} Selected:")
        print(f"Title: {selected_task['title']}")
        print(f"Description: {selected_task['description']}")
        print(f"Due Date: {selected_task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Assigned Date: {selected_task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
        print(f"Completed: {'Yes' if selected_task['completed'] else 'No'}")
        print()
        # give the user the option to mark task as complete or edit who it is assigned to as requested
        while True:
            choice = input("Enter 'c' to mark the task as complete or 'e' to edit the task: ")
            if choice == 'c':
                selected_task['completed'] = True
                print("Task marked as complete.")
                break
            elif choice == 'e':
                if selected_task['completed']:
                    print("Task is already completed. You cannot edit it.")
                    break

                new_username = input("Enter the new username for the task: ")
                new_due_date = input("Enter the new due date for the task (YYYY-MM-DD): ")
                try:
                    new_due_date = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                except ValueError:
                    print("Invalid datetime format. Please try again.")
                    continue

                selected_task['username'] = new_username
                selected_task['due_date'] = new_due_date
                print("Task edited successfully.")
                break
            else:
                print("Invalid choice. Please try again.")

# Function to generate reports
def generate_report():
    num_users = len(username_password.keys())
    total_tasks = len(task_list)
    completed_tasks = sum(t['completed'] for t in task_list)
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(t['due_date'] < datetime.combine(date.today(), datetime.min.time()) and not t['completed'] for t in task_list)
    incomplete_percentage = (uncompleted_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    overdue_percentage = (overdue_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write("Task Overview\n")
        task_overview_file.write("----------------\n")
        task_overview_file.write(f"Total Tasks: {total_tasks}\n")
        task_overview_file.write(f"Completed Tasks: {completed_tasks}\n")
        task_overview_file.write(f"Uncompleted Tasks: {uncompleted_tasks}\n")
        task_overview_file.write(f"Overdue Tasks: {overdue_tasks}\n")
        task_overview_file.write(f"Incomplete Tasks Percentage: {incomplete_percentage:.2f}%\n")
        task_overview_file.write(f"Overdue Tasks Percentage: {overdue_percentage:.2f}%\n")

    user_stats = []
    for username in username_password.keys():
        user_tasks = sum(t['username'] == username for t in task_list)
        user_completed = sum(t['username'] == username and t['completed'] for t in task_list)
        user_incomplete = sum(t['username'] == username and not t['completed'] for t in task_list)
        user_overdue = sum(t['username'] == username and t['due_date'] < datetime.combine(date.today(), datetime.min.time()) and not t['completed'] for t in task_list)
        user_total_percentage = (user_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        user_completed_percentage = (user_completed / user_tasks) * 100 if user_tasks > 0 else 0
        user_incomplete_percentage = (user_incomplete / user_tasks) * 100 if user_tasks > 0 else 0
        user_overdue_percentage = (user_overdue / user_tasks) * 100 if user_tasks > 0 else 0
        user_stats.append((username, user_tasks, user_total_percentage, user_completed_percentage,
                           user_incomplete_percentage, user_overdue_percentage))

    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write("User Overview\n")
        user_overview_file.write("----------------\n")
        user_overview_file.write(f"Total Users: {num_users}\n")
        user_overview_file.write(f"Total Tasks: {total_tasks}\n")
        user_overview_file.write("----------------\n")
        for user_stat in user_stats:
            user_overview_file.write(f"Username: {user_stat[0]}\n")
            user_overview_file.write(f"Total Tasks Assigned: {user_stat[1]}\n")
            user_overview_file.write(f"Percentage of Total Tasks: {user_stat[2]:.2f}%\n")
            user_overview_file.write(f"Percentage of Completed Tasks: {user_stat[3]:.2f}%\n")
            user_overview_file.write(f"Percentage of Incomplete Tasks: {user_stat[4]:.2f}%\n")
            user_overview_file.write(f"Percentage of Overdue Tasks: {user_stat[5]:.2f}%\n")
            user_overview_file.write("----------------\n")

# Function to display statistics
def display_statistics():
    # Check if the reports exist, if not, generate them
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        generate_report()

    # Read and display the task overview report
    with open("task_overview.txt", "r") as task_report_file:
        task_report = task_report_file.read()
        print("Task Overview Report:")
        print(task_report)

    # Read and display the user overview report
    with open("user_overview.txt", "r") as user_report_file:
        user_report = user_report_file.read()
        print("User Overview Report:")
        print(user_report)

while True:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my tasks
ds - Display statistics
gr - Generate reports
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine()
    elif menu == 'ds' and curr_user == 'admin':
        display_statistics()
    elif menu == 'gr':
        generate_report()
        print("Reports generated successfully.")
    elif menu == 'e':
        print('Thank you for using Task Manager!')
        exit()
    else:
        print("You have made a wrong choice. Please try again.")
