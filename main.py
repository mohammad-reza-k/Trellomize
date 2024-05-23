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
from datetime import datetime, timedelta

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

taskjson = "tasks.json"
projson = "projects.json"
members = "members.json"
memberstask = "memberstask.json"
descrip = "descriptionstask.json"
projects_by_user = {}
task_by_user = {}
memberdic = {}
membertaskdic = {}
des = {}
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

def delete_project(user,project_name_to_delete):
    # Read the existing tasks from the file
    with open('projects.txt', 'r') as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        user_name, project_name = line.strip().split(' ')
        if project_name != project_name_to_delete:
            updated_lines.append(line)
    with open('projects.txt', 'w') as file:
        file.writelines(updated_lines)
        
    if project_name_to_delete in projects_by_user:
        del task_by_user[project_name_to_delete]
    save_data(task_by_user, taskjson)
    
    if user in projects_by_user:
        del projects_by_user[user]
    save_data(projects_by_user, projson)
    updated = []
    with open('tasks.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            project_name, task_name , di= line.strip().split(' ')
            if project_name != project_name_to_delete:
                updated.append(line)
    with open('tasks.txt', 'w') as f:
        f.writelines(updated)

    with open('members.txt', 'r') as file:
        lines = file.readlines()

    update = []
    for line in lines:
        project_name, member_name = line.strip().split(' ')
        if project_name != project_name_to_delete:
            update.append(line)
    with open('members.txt', 'w') as file:
        file.writelines(updated_lines)
        
    if project_name_to_delete in memberdic:
        del memberdic[project_name_to_delete]
    save_data(memberdic, members)

    return projects_by_user

    
def add_task():
    with open('tasks.txt', 'r') as file:
        for line in file:
            project_name, task_name, *description = line.strip().split(' ', 2)
            description = ' '.join(description)  # Join the remaining elements as description
            if project_name in task_by_user:
                if task_name not in task_by_user[project_name]:
                    task_by_user[project_name].append(task_name)
            else:
                task_by_user[project_name] = [task_name]
    save_data(task_by_user, taskjson)
    return task_by_user

def add_description():
      # Initialize an empty dictionary to store descriptions
    with open('tasks.txt', 'r') as file:
        for line in file:
            # Split the line only twice to separate project_name and task_name,
            # and then combine the remaining elements as description
            project_name, task_name, *description = line.strip().split(' ', 2)
            description = ' '.join(description)  # Join the remaining elements as description
            des[task_name] = description
    save_data(des, descrip)  # Save the descriptions to a file
    return des

def delete_task(task_name_to_delete):
    # Read the existing tasks from the file
    with open('tasks.txt', 'r') as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        project_name, task_name, *description = line.strip().split(' ', 2)
        description = ' '.join(description)  # Join the remaining elements as description
        if task_name != task_name_to_delete:
            updated_lines.append(line)

    with open('tasks.txt', 'w') as file:
        file.writelines(updated_lines)

    if task_name_to_delete in task_by_user:
        del task_by_user[task_name_to_delete]
    save_data(task_by_user, taskjson)
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

def delete_members(member_name_to_delete):
    with open('members.txt', 'r') as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        project_name, member_name = line.strip().split(' ')
        if member_name != member_name_to_delete:
            updated_lines.append(line)

    with open('member.txt', 'w') as file:
        file.writelines(updated_lines)

    if member_name_to_delete in memberdic:
        del memberdic[member_name_to_delete]
    return memberdic#delete member from project

def add_member_to_task():
    with open('memberstask.txt', 'r') as file:
        for line in file:
            project_task_name, member_name = line.strip().split(' ')  
            if project_task_name in membertaskdic:
                if member_name not in membertaskdic[project_task_name]:
                    membertaskdic[project_task_name].append(member_name)
            else:
                membertaskdic[project_task_name] = [member_name]
    save_data(membertaskdic, memberstask)
    return membertaskdic

   
def save_data(data_dic, files):
    with open(files, 'w') as json_file:
        json.dump(data_dic, json_file, indent=4)

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

class Task:
    def __init__(self, title, description, assigned_to, priority, status):
        self.title = title
        self.description = description
        self.assigned_to = assigned_to
        self.priority = priority
        self.status = status

class Project:
    def __init__(self, title, creator):
        self.title = title
        self.creator = creator

    def create_task(self, title, description, priority, status):
        with open("tasks.txt", 'a') as f:
            f.write(f"{self.title} {title} {description}\n")
            add_task()
        current_time = datetime.now()
        end_time = current_time + timedelta(hours=24)
        with open("time.txt", 'a') as f:
            f.write(f"{self.title} {title} {current_time} {end_time}\n")

        with open("task_details.txt", 'a') as f:
            f.write(f"{self.title} {title} {priority.name} {status.name}\n")

    def assign_task(self, assigned_to_task, name):
        with open('memberstask.txt', 'a') as f:
            f.write(f"{self.title}{assigned_to_task} {name}\n")
            add_member_to_task()

    def add_member(self, username):
        with open("members.txt", 'a') as f:
            f.write(f"{self.title} {username}\n")
            add_members()

def return_project(title, creator):
    return Project(title, creator)

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.is_activate = True

    def create_project(self, title):
        with open("projects.txt", 'a') as f:
            f.write(f"{self.username} {title}\n") 
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
            f.write(f"{email} {username} {hashh(password)} T\n") 
            f.close()
            with open("manage.txt", "a") as file:
                file.write(email)
                file.write(" \n")#admin

        return User(username, password)
    else:
        console.print("[bold red]Invalid email, username, or password. Please try again.[/bold red]")
        return None
def tedad_vorood(word, file_path):
     with open(file_path, 'r+') as file:
         content = file.read()
         word_start = content.find(word)
        
         if word_start == -1:  # Word not found
             print(f"Word '{word}' not found in the file.")
             return
        
         number_start = word_start + len(word)  # Start index of the number
         while number_start < len(content) and content[number_start] == ' ':
             number_start += 1
        
         number_end = number_start

         # Find the end of the number
         while number_end < len(content) and content[number_end].isdigit():
             number_end += 1

         if number_start == number_end:  # No number found after the word
             number = 1
             new_content = content[:number_start] + " 1" + content[number_end:]
         else:
             number = int(content[number_start:number_end]) + 1
             new_content = content[:number_start] + str(number) + content[number_end:]
        
         # Move the file cursor to the beginning and write the new content
         file.seek(0)
         file.write(new_content)
         file.truncate()#admin
         
def check_admin(username , passw):
    a = 0
    with open ("adminfile.txt" , "r") as file:
        content = file.read()
        if (username and passw) in content:
            a = 1
        
    return a# admin

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
            choice = Prompt.ask("\nSelect an option:\n1. Create Project\n2. View Projects\n3. View Other User\n4. Go back\n")
            if choice == "1":
                clear_console()
                title = Prompt.ask("Enter project title:")
                user.create_project(title)
                console.print("[bold blue]Project created successfully![/bold blue]")
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
                                        table.add_row(f"{dic[i][j]}", f"{dicm[dic[i][j]]}")#table project
                                    else:
                                        table.add_row(f"{dic[i][j]}", "No members yet")
                        console.print(table)
                        ch = Prompt.ask("\n1.delete project \n2.View tasks\n3.Assigne tasks\n4.add members/view members\n5.Go back and refresh\n")
                        if ch=='2':
                            clear_console()
                            project = Prompt.ask("Enter your projects name you want:\n")
                            if project in dic[user.username]:
                                dicc = add_task()
                                if project in dicc.keys():
                                #view tasks are in
                                    while True:
                                        di = add_member_to_task()
                                        pro = return_project(project, user.username)
                                        tabl = Table(title="Your Tasks")
                                        tabl.add_column("Name", style="cyan", no_wrap=True)
                                        tabl.add_column("Members Assigned", style="magenta")
                                        tabl.add_column("Description", style="magenta")
                                        
                                        for i in dicc:
                                            if i==project:
                                                for j in range(len(dicc[i])):
                                                    des = add_description()
                                                    if i+dicc[i][j] in di:
                                                        tabl.add_row(f"{dicc[i][j]}", f"{di[i+dicc[i][j]]}", f"{des[dicc[i][j]]}")#tabel task
                                                    else:
                                                        tabl.add_row(f"{dicc[i][j]}", 'No assignment yet', f"{des[dicc[i][j]]}")#########changing description
                                        console.print(tabl)
                                        option = Prompt.ask("1.add new task\n2.delete task\n3.Go back\n")
                                        if option == '1':
                                            clear_console()
                                            name = Prompt.ask("Enter the Name of the task:")
                                            description = Prompt.ask("what description for the task you want to add:")
                                            priority = Prompt.ask("Enter the priority (m for medium, c for critical, h for high, nothing for low)")
                                            if priority == 'm':
                                                pro.create_task(name, description, Priority.MEDIUM, Status.BACKLOG)
                                                pro.create_task(name, description, Priority.MEDIUM, Status.BACKLOG)#refresh

                                            elif priority == 'c':
                                                pro.create_task(name, description, Priority.CRITICAL, Status.BACKLOG)
                                                pro.create_task(name, description, Priority.CRITICAL, Status.BACKLOG)#refresh

                                            elif priority == 'h':
                                                pro.create_task(name, description, Priority.HIGH, Status.BACKLOG)
                                                pro.create_task(name, description, Priority.HIGH, Status.BACKLOG)#refresh

                                            else:
                                                pro.create_task(name, description, Priority.LOW, Status.BACKLOG)
                                                pro.create_task(name, description, Priority.LOW, Status.BACKLOG)#refresh


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
                                    console.print("[bold yellow]No tasks yet[/bold yellow]\n")
                                    pro = return_project(project, user.username)
                                    option = Prompt.ask("1.add new task\n2.delete a task\n3.Go back\n")
                                    if option == '1':
                                        clear_console()
                                        name = Prompt.ask("Enter the Name of the task:")
                                        discription = Prompt.ask("what description for the task you want to add:")
                                        pro.create_task(name, discription, Priority.LOW, Status.BACKLOG)
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
                                console.print("[bold red]No such a project[/bold red]\n")
                        elif ch == '3':
                            clear_console()
                            option = Prompt.ask("Enter name of a project")#and check meber and task and check task and add to a file 
                            taskkk = Prompt.ask("Enter name of a task you want to assigne") 
                            memb = Prompt.ask("Enter name of the member you want to add")
                            dicc = add_task()
                            for i in dic[user.username]:
                                if i != option:
                                    console.print(f"[bold red]No such a project named '{option}'[/bold red]\n")
                                else:
                                    if not option in dicc:
                                        console.print(f"[bold red]No tasks in '{option}'[/bold red]\n")
                                    else:
                                        for j in dicc[option]:
                                            if j != taskkk:
                                                console.print(f"[bold red]No such a task named '{taskkk}'[/bold red]\n")
                                            else:
                                                dicm = add_members()
                                                if not option in dicm:
                                                   console.print(f"[bold red]No members in '{option}'[/bold red]\n") 
                                                elif not memb in dicm[option]:
                                                    console.print(f"[bold red]No member named '{memb}' in project '{option}'[/bold red]\n") 
                                                else:
                                                    di = add_member_to_task()
                                                    if len(di)==0:
                                                        pro = return_project(option, user.username)
                                                        pro.assign_task(taskkk, memb, 'low')
                                                    else:
                                                        if not option+taskkk in di:
                                                            console.print("[bold red]No members assigned[/bold red]")
                                                        else:
                                                            a=0 #couter for adding
                                                            for z in di[option+taskkk]:
                                                                if z == memb and a==0:
                                                                    console.print(f"[bold yellow]user {memb} is already in project '{option}' and task '{taskkk}'[/bold yellow]")#return??
                                                                    a=1
                                                            if a==0:
                                                                pro = return_project(option, user.username)
                                                                pro.assign_task(taskkk, memb, 'low')
                                                            
                                                                #pro.assign_task(taskkk, memb)#refresh??
                                
                        elif ch == '5':
                            clear_console()
                            break
                        elif ch =='4':
                            clear_console()
                            
                            project = Prompt.ask("the name of the project")
                            if project in dic[user.username]:
                                d = add_members()
                                member = Prompt.ask("Enter username or a email of the one you want to add to your project:")
                                pro = return_project(project, user.username)
                                a=0 #counter for adding member onc
                                with open('manba.txt', 'r') as file:                                
                                    for line in file:
                                        email, nam,ram, t=line.strip().split(' ') 
                                        if len(d)==0:
                                            if (member==email or member==nam) and a==0:
                                                pro.add_member(member)
                                                pro.add_member(member)#refresh
                                                console.print('[bold green]Member added successfully![/bold green]')
                                                a=1

                                        else:
                                            if project in d and member in d[project]:
                                                a=2
                                            elif (member==email or member==nam) and a==0:
                                                pro.add_member(member)
                                                pro.add_member(member)#refresh
                                                console.print('[bold green]Member added successfully![/bold green]')
                                                a=1
                                                break

                                    if a==0:
                                        console.print(f"[bold red]No user account named '{member}' found[/bold red]")      
                                    if a==2:
                                        console.print(f"[bold yellow]user '{member}' is already in the project[/bold yellow]")
                                
                            else:
                                console.print("[bold red]No such a project[/bold red]\n")#return??
                        elif ch == '1':
                            clear_console()
                            proro = Prompt.ask("Name of the project you want to delete:")
                            for i in dic:
                                if i==user.username:
                                    if proro in dic[i]:
                                        dic[user.username].remove(proro)
                                        delete_project(user.username,proro)
                                        break
                                    else:
                                        console.print("[bold yellow]No such a project[/bold yellow]\n") 

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
