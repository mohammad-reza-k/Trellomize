from rich.prompt import Prompt
from rich.console import Console
from datetime import datetime
from enum import Enum, auto
import hashlib
import os
import uuid
import json
file = "data.json"
data = {
    "username": [],
    "email": [],
    "password": [],
    "projects": [
        {
            "titles": [],
            "members": {"usernames":[]},
            "tasks": [{"names":[{"assighnees":[]}]}]
        }
    ]
}

def load_data():
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "username": [],
            "email": [],
            "password": [],
            "projects": [
                {
                    "titles": [],
                    "members": {"usernames":[]},
                    "tasks": [{"names":[{"assighnees":[]}]}]
                }
            ]
        }
        
def save_data(data_dic):
    with open(file, 'w') as json_file:
        json.dump(data_dic, json_file, indent=4)

def appendt(data_dic, value):
    for project in data_dic["projects"]:
        project['titles'].append(value)
        
def appendm(data_dic, value):
    for project in data_dic["projects"]:
            project['members']["usernames"].append(value)
            
def appendas(data_dic, value):
    for project in data_dic["projects"]:
            for tasks in project["tasks"]:
                for name in tasks["names"]:
                    name["assignees"].append(value)#assighn
def appendn(data_dic, value):
    for project in data_dic["projects"]:
            for tasks in project["tasks"]:
                tasks["names"].append(value)
            
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
    def __init__(self, title, description='', start_date=None, end_date=None, priority=Priority.LOW, status=Status.BACKLOG):
        self.assignees=[]
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.priority = priority
        self.status = status
        
class Project:
    def __init__(self, title, creator):
        self.title = title
        self.creator = creator
        self.tasks = []
        self.members = []

    def create_task(self, title, description):
        task = Task(title, description, None, None, None, None)
        self.tasks.append(task)
        data_dic=load_data()
        appendn(data_dic, task.title)
        # data_dic["projects"][0]["tasks"]["names"].append(task.title)
        save_data(data_dic)
        
    def assign_task(self, title, assigned_to):
        for task in self.tasks:
            if task.title == title:
                task.assigned_to = assigned_to
                # Assuming 'assigned_to' is a username, find or create the User object
                member = next((m for m in self.members if m.username == assigned_to), None)
                if not member:
                    member = User(assigned_to, None)  # Replace None with actual password if available
                    self.members.append(member)
                    data_dic=load_data()
                    appendas(data_dic, member.username)
                    #data_dic["projects"]["names"]["assighnees"].append(member.username)
                    save_data(data_dic)
                return True
        return False

    # def modify_task(self, task_id, title=None, description=None, assigned_to=None):
    #     for task in self.tasks:
    #         if task.task_id == task_id:
    #             if title:
    #                 task.title = title
    #             if description:
    #                 task.description = description
    #             if assigned_to:
    #                 task.assigned_to = assigned_to
    #             return True
    #     return False

    def add_member(self, username):
        member = User(username, None)  
        self.members.append(member)
        data_dic=load_data()
        appendm(data_dic, member.username)
        #data_dic["projects"]["members"]["usernames"].append(member.username)
        save_data(data_dic)
        
    def view_members(self):
        if len(self.members) == 0:
            print("No users yet\n")
        else:
            for member in self.members:
                print(f"\nMembers:\n{member.username}\n")

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.projects = []
        self.is_activate = False


    def create_project(self, title):
        project = Project(title, self.username)
        self.projects.append(project)
        data_dic=load_data()
        appendt(data_dic, project.title)
        #data_dic["projects"].append(["title"].append(project.title))
        save_data(data_dic) 
               
def create_acc():
    console = Console()
    email = Prompt.ask("Enter your email:")
    if login(email)==1:
        print("You Already Have An Account")
        return
    username = Prompt.ask("Enter your username:")
    password = Prompt.ask("Enter your password:", password=True)
    if email.endswith(".com") and '@' in email and len(password) >= 5:
        console.print("[bold green]Login successful![/bold green]")
        data_dic=load_data()
        data_dic["username"].append(username)
        data_dic["email"].append(email)
        data_dic["password"].append(hashh(password))
        save_data(data_dic)
        return User(username, password)
    else:
        console.print("[bold red]Invalid email, username, or password. Please try again.[/bold red]")
        return None
def login_acc(username, password):
    return User(username, password)

def login(esm):
    a = 0
    with open (file , "r") as f:
        content = json.load(f)
        if esm in content["username"]:
            a = 1
    return a

def check_pass(input_email_orUser, input_password):
    try:
        data_dic = load_data()
        for email, username, password in zip(data_dic['email'], data_dic['username'], data_dic['password']):
            if (email == input_email_orUser or username == input_email_orUser) and password == input_password:
                return True
    except Exception as e:
        print(f"An error occurred: {e}")
    return False
    

def display_user_page(user):
    console = Console()
    console.print(f"Welcome, [blue]{user.username}![/blue]")
    while True:
        choice = Prompt.ask("\nSelect an option:\n1. Create Project\n2. View Projects\n3. View Other User\n4. Exit\n")
        if choice == "1":
            title = Prompt.ask("Enter project title:")
            user.create_project(title)
            console.print("[bold green]Project created successfully![/bold green]")
        elif choice == "2":
            json.load(file)
            if not file["projets"]["tasks"]:
                console.print("[bold yellow]You have no projects yet.[/bold yellow]")
            else:
                console.print("[bold blue]Your Projects:[/bold blue]")
                # for project in user.projects:
                #     console.print(f"Project ID: {project.project_id}, Title: {project.title}, Creator: {project.creator}")
                #     project.add_member(user.username)
                
                    # Added logic to view and add members
                for project in user.projects:
                    ch = Prompt.ask("\n1.View Members\n2.Add Member")
                    if ch == '1':
                        project.view_members()
                    elif ch == '2':
                        username_to_add = Prompt.ask("Enter username to add:")
                        if username_to_add in project:
                            print("Already exist\n")
                        else:
                            project.add_member(username_to_add)
                            console.print("[bold green]Member added successfully![/bold green]")
        elif choice == "3":
            username_to_view = Prompt.ask("Enter username of the user you want to view:")
            console.print(f"[bold blue]Viewing profile of user: {username_to_view}[/bold blue]")
        elif choice == "4":
            console.print("[bold]Goodbye![/bold]")
            break
        else:
            console.print("[bold red]Invalid choice. Please select a valid option.[/bold red]")


def hashh(password):
    p = hashlib.sha256(password.encode("utf-8")).digest()
    return p.hex()

def dis_hashh(password):
    h = hashlib.sha256(password.encode("utf-8")).digest()
    return h.hex()

def main():
    console = Console()
    while True:
        choice = Prompt.ask("\nSelect an option:\n1. Create Account\n2. Login\n3. Exit\n")
        if choice == "1":
            user = create_acc()
            if user:
                display_user_page(user)
        elif choice == "2" :
            nam= Prompt.ask("enter your email or username")
            ramz = Prompt.ask("Enter Your Password:", password=True)
            if check_pass(nam, hashh(ramz)):
                console.print("[bold green]log in sucsusfully![/bold green]\n")
                user = login_acc(nam, ramz)
                display_user_page(user) 
            elif not check_pass(nam, ramz):
                print("ٌWrong username, email or password!!\n")
                return
        elif choice == "3":
            console.print("[bold]Goodbye![/bold]")
            exit()
        else:
            console.print("[bold red]Invalid choice. Please select a valid option.[/bold red]")

if __name__ == "__main__":
    main()
