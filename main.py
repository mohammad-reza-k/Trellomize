from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
import hashlib
import os
import uuid
import fontstyle
from datetime import datetime
from enum import Enum, auto
import json
import time
import manager
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

taskjson = "tasks.json"
projson = "projects.json"
members = 'members.json'
projects_by_user = {}
task_by_user = {}
memberdic = {}

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def add_project():
    try:
        with open('projects.txt', 'r') as file:
            for line in file:
                username, project_name = line.strip().split(' ')  
                if username in projects_by_user:
                    if project_name not in projects_by_user[username]:
                        projects_by_user[username].append(project_name)
                else:
                    projects_by_user[username] = [project_name]
        save_data(projects_by_user, projson)
        return projects_by_user
    except Exception as e:
        logging.error(f'Error in add_project function: {e}', exc_info=True)
        
def add_task():
    with open('tasks.txt', 'r') as file:
        for line in file:
            project_name, task_name, discription = line.strip().split(' ')  
            if project_name in task_by_user:
                if task_name not in task_by_user[project_name]:
                    task_by_user[project_name].append(task_name)
            else:
                task_by_user[project_name] = [task_name]
    save_data(task_by_user, taskjson)
    return task_by_user

def delete_task(task_name_to_delete):
    # Read the existing tasks from the file
    with open('tasks.txt', 'r') as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        project_name, task_name, description = line.strip().split(' ')
        if task_name != task_name_to_delete:
            updated_lines.append(line)

    with open('tasks.txt', 'w') as file:
        file.writelines(updated_lines)

    if task_name_to_delete in task_by_user:
        del task_by_user[task_name_to_delete]
    return task_by_user
    
    
def add_members():
    with open('members.txt', 'r') as file:
        for line in file:
            project_name, member_name = line.strip().split(' ')  
            if project_name in memberdic:
                if member_name not in memberdic[project_name]:
                    memberdic[project_name].append(member_name)
            else:
                memberdic[project_name] = [member_name]
    save_data(memberdic, members)
    return memberdic

    
class Task:
    def __init__(self, title, description, assigned_to):
        self.title = title
        self.description = description
        self.assigned_to = assigned_to

class Priority(Enum):
    CRITICAL = auto()
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()

class Status(Enum):
    BACKLOG = auto()
    TODO = auto()
    DOING = auto()
    DONE = auto()
    ARCHIVED = auto()

# def load_data(files):
#     try:
#         with open(files, 'r') as f:
#             return json.load(f)
#     except FileNotFoundError:
#         return {
#             "tasks":[],
#             "members":[],
#             "taskassigne":[]
            
#         }

def save_data(data_dic, files):
    with open(files, 'w') as json_file:
        json.dump(data_dic, json_file, indent=4)

class Project:
    def __init__(self, title, creator):
        self.title = title
        self.creator = creator

    def create_task(self, title, description):
        with open("tasks.txt", 'a') as f:
            f.write(self.title)
            f.write(' ')
            f.write(title)
            f.write(' ')
            f.write(description)
            f.write('\n')
            add_task()

    def assign_task(self, title, assigned_to):
        # dic = load_data(projson)
        # for task in dic["tasks"]:
        #     if task == title:
        #         dic["taskassigne"].append(assigned_to)
        #         save_data(dic, projson)
        #         # Assuming 'assigned_to' is a username, find or create the User object
        #         member = next((m for m in dic["members"] if m == assigned_to), None)
        #         if not member:
        #             member = User(assigned_to, None)  # Replace None with actual password if available
        #             # self.members.append(member)
        #         return True
        # return False#dtylk;kljghk
        pass

    # def modify_task(self, title=None, description=None, assigned_to=None):
    #     for task in self.tasks:
    #         if task.title == title:
    #             if description:
    #                 task.description = description
    #             if assigned_to:
    #                 task.assigned_to = assigned_to
    #             return True
    #     return False

    def add_member(self, username):
        with open("members.txt", 'a') as f:
            f.write(self.title)
            f.write(' ')
            f.write(username)
            f.write('\n')
            add_members()
        
def return_project(title, creator):
    return Project(title,creator)

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.is_activate = True

    def create_project(self, title):
        project = Project(title, self.username)
        with open("projects.txt", 'a') as f:
            f.write(self.username) 
            f.write(" ")
            f.write(title)
            f.write("\n") 
            f.close()
            add_project()
        
def create_acc():
    console = Console()
    email = Prompt.ask("Enter your email:")
    if login(email)==1:
        console.print("[bold blue]this account already exist[/bold blue]\n")
        return
    username = Prompt.ask("Enter your username:")
    password = Prompt.ask("Enter your password:", password=True)
    if email.endswith(".com") and '@' in email and len(password) >= 5:
        console.print("[bold green]Login successful![/bold green]")
        with open("manba.txt","a") as f:
            f.write(email) 
            f.write(" ")
            f.write(username)
            f.write(" ")
            f.write(hashh(password))
            f.write(" ")
            f.write("T")
            f.write("\n") 
            f.close()
            with open("manage.txt", "a") as file:
                file.write(email)
                file.write(" \n")

        return User(username, password)
    else:
        console.print("[bold red]Invalid email, username, or password. Please try again.[/bold red]")
        return None
# def tedad_vorood(word, file_path):
#     with open(file_path, 'r+') as file:
#         content = file.read()
#         word_start = content.find(word)
        
#         if word_start == -1:  # Word not found
#             print(f"Word '{word}' not found in the file.")
#             return
        
#         number_start = word_start + len(word)  # Start index of the number
#         while number_start < len(content) and content[number_start] == ' ':
#             number_start += 1
        
#         number_end = number_start

#         # Find the end of the number
#         while number_end < len(content) and content[number_end].isdigit():
#             number_end += 1

#         if number_start == number_end:  # No number found after the word
#             number = 1
#             new_content = content[:number_start] + " 1" + content[number_end:]
#         else:
#             number = int(content[number_start:number_end]) + 1
#             new_content = content[:number_start] + str(number) + content[number_end:]
        
#         # Move the file cursor to the beginning and write the new content
#         file.seek(0)
#         file.write(new_content)
#         file.truncate()

def check_admin(username , passw):
    a = 0
    with open ("adminfile.txt" , "r") as file:
        content = file.read()
        if (username and passw) in content:
            a = 1
        
    return a

def login_acc(username, password):
    return User(username, password)
def login(username):
    a = 0
    with open ("manba.txt" , "r") as file:
        content = file.read()
        if username in content:
            a = 1
    return a

        
def check_pass(input_email_orUser, input_password, file_path):
    console = Console()
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for i in range(0, len(lines), 1):  # Increment by 1 to read each line
            email, username, password, act = lines[i].strip().split()  # Split each line into email, username, and password
            
            if (email == input_email_orUser or username == input_email_orUser) and password == input_password and act=="T":
                return True
            if act == "F":
                console.print("[bold red]you are baned go to the manager[/bold red]")
                
    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")
    return False
    

def display_user_page(user):
    console = Console()
    print(fontstyle.apply(f"Well come {user.username}", 'bold/italic/green'))
    while True:
            choice = Prompt.ask("\nSelect an option:\n1. Create Project\n2. View Projects\n3. View Other User\n4. Exit\n")
            if choice == "1":
                clear_console()
                title = Prompt.ask("Enter project title:")
                user.create_project(title)
                console.print("[bold green]Project created successfully![/bold green]")
            elif choice == "2":
                clear_console()
                dic = add_project()
                dicm = add_members()
                if not user.username in dic.keys():
                    console.print("[bold yellow]You have no projects yet.[/bold yellow]")
                else:
                    while True:

                        table = Table(title="Your Projects")
                        table.add_column("Name", style="cyan", no_wrap=True)
                        table.add_column("Members", style="magenta")
                        for i in dic:
                            if i==user.username:
                                for j in range(len(dic[i])):
                                    if dic[i][j] in dicm:
                                        table.add_row(f"{dic[i][j]}", f"{dicm[dic[i][j]]}")
                                    else:
                                        table.add_row(f"{dic[i][j]}", "No members yet")
                        console.print(table)
                        ch = Prompt.ask("\n1.View Tasks \n2.Assigne tasks\n3.Exit\n4.add members/view members \n")
                        if ch=='1':
                            clear_console()
                            project = Prompt.ask("Enter your projects name you want:\n")
                            if project in dic[user.username]:
                                dicc = add_task()
                                if project in dicc.keys():
                                #view tasks are in
                                    while True:
                                        pro = return_project(project, user.username)
                                        tabl = Table(title="Your Tasks")
                                        tabl.add_column("Name", style="cyan", no_wrap=True)
                                        tabl.add_column("Members", style="magenta")
                                        for i in dicc:
                                            if i==project:
                                                for j in range(len(dicc[i])):
                                                    tabl.add_row(f"{dicc[i][j]}", "r")
                                        console.print(tabl)
                                        option = Prompt.ask("1.add new task\n2.delete a task\n3.exit\n")
                                        if option == '1':
                                            clear_console()
                                            name = Prompt.ask("Enter the Name of the task:")
                                            discription = Prompt.ask("what dis cription for the task you want to add:")
                                            pro.create_task(name, discription)
                                            pro.create_task(name, discription)#refresh

                                            console.print("[bold blue]Task Created successfully![/bold blue]\n")
                                        #new task with priority
                                        elif option == '2':
                                            clear_console()
                                            taskk = Prompt.ask("Name of the task you want to delete:")
                                            for i in dicc:
                                                if i==project:
                                                    if taskk in dicc[i]:
                                                        dicc[project].remove(taskk)
                                                        delete_task(taskk)
                                                    else:
                                                        console.print("[bold yellow]No such a task in your project[/bold yellow]\n") 
                                            
                                        elif option == '3':
                                            clear_console()
                                            break
                                        else:
                                            clear_console()
                                            console.print("[bold red]invalid choice[/bold red]\n")
                                            
                                else:
                                    clear_console()
                                    console.print("No tasks yet\n")#return??
                                    pro = return_project(project, user.username)
                                    option = Prompt.ask("1.add new task\n2.delete a task\n3.exit\n")
                                    if option == '1':
                                        clear_console()
                                        name = Prompt.ask("Enter the Name of the task:")
                                        discription = Prompt.ask("what dis cription for the task you want to add:")
                                        pro.create_task(name, discription)
                                        pro = return_project(project, user.username)
                                    #new task with priority
                                    elif option == '2':
                                            clear_console()
                                            taskk = Prompt.ask("Name of the task you want to delete:")
                                            for i in dicc:
                                                if i==project:
                                                    if taskk in dicc[i]:
                                                        dicc[project].remove(taskk)
                                                        delete_task(taskk)
                                                    else:
                                                        console.print("[bold yellow]No such a task in your project[/bold yellow]\n") 

                                    else:
                                        clear_console()
                                        break

                            else:
                                clear_console()
                                console.print("[bold red]No such a project[/bold red]\n")#return??
                        elif ch == '2':
                            clear_console()
                            option = Prompt.ask("Enter name of a member")#and check meber and task and check task and add to a file 
                            
                        elif ch == '3':
                            clear_console()
                            break
                        elif ch=='4':
                            clear_console()
                            
                            project = Prompt.ask("the name of the project")
                            if project in dic[user.username]:
                                member = Prompt.ask("Enter username or a email of the one you want to add to your project:")
                                pro = return_project(project, user.username)
                                
                                with open('manba.txt', 'r') as file:
                                    a=0 #counter for adding member once                                 
                                    for line in file:
                                        if member in line and a==0:
                                            pro.add_member(member)
                                            pro.add_member(member)#refresh
                                            console.print('[bold green]Member added successfully![/bold green]')
                                            a+=1
                                        elif a>=1:
                                            pass
                                        else:
                                            console.print(f'[bold red]No such a user named {member}[/bold red]\n')
                            else:
                                console.print("[bold red]No such a project[/bold red]\n")#return??

                        else:
                            clear_console()
                            console.print("[bold yellow]Invalid choice[/bold yellow]\n")
 
            elif choice == "3":
                clear_console()
                username_to_view = Prompt.ask("Enter username of the user you want to view:")
                console.print(f"[bold blue]Viewing profile of user: {username_to_view}[/bold blue]")
            elif choice == "4":
                clear_console()
                break
            else:
                clear_console()
                console.print("[bold red]Invalid choice. Please select a valid option.[/bold red]")

def hashh(password):
    p = hashlib.sha256(password.encode("utf-8")).digest()
    return p.hex()

def dis_hashh(password):
    h = hashlib.sha256(password.encode("utf-8")).digest()
    return h.hex()

def main():
    console = Console()
    x = 0
    while True:
        choice = Prompt.ask("\nSelect an option:\n1. Create Account\n2. Login\n3. Exit\n")
        if choice == "1":
            clear_console()
            user = create_acc()
            if user:
                display_user_page(user)
        elif choice == "2" :
            clear_console()
            nam= Prompt.ask("enter your email or username\n")
            ramz = Prompt.ask("Enter Your Pass:\n")
            # if check_admin(nam , ramz ):
            #     print("meow")

            if check_pass(nam, hashh(ramz), "manba.txt"):
                console.print("[bold green]log in sucsusfully![/bold green]\n")
                user = login_acc(nam, ramz)
                display_user_page(user) 
            elif not check_pass(nam, ramz, "manba.txt"):
                x+=1
                console.print(f"[bold red]Wrong username, email or password!![/bold red]\n[yellow]attemp {x} of 4[/yellow]\n")
                if x == 4:
                    console.print("[bold red]try again later[/bold red]")
                    exit()
                    
        elif choice == "3":
            clear_console()
            console.print("[bold red]Goodbye![/bold red]")
            exit()
        else:
            clear_console()
            x+=1
            console.print(f"[bold red]Invalid choice. Please select a valid option.[/bold red]\n[yellow]attemp {x} of 4[/yellow]\n")
            if x == 4:
                console.print("[bold red]try again later[/bold red]")
                exit()


if __name__ == "__main__":
    main()
