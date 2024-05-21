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
import re

file = "tasks.json"
projects_by_user = {}


def add_project():
    with open('projects.txt', 'r') as file:
        for line in file:
            username, project_name = line.strip().split(' ')  
            if username in projects_by_user:
                if project_name not in projects_by_user[username]:
                    projects_by_user[username].append(project_name)
            else:
                projects_by_user[username] = [project_name]
    save_data(projects_by_user)
    return projects_by_user

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

def load_data():
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "tasks":[],
            "members":[],
            "taskassigne":[],
            "taskdiscription":[]
        }

def save_data(data_dic):
    with open(file, 'w') as json_file:
        json.dump(data_dic, json_file, indent=4)

class Project:
    def __init__(self, title, creator):
        self.title = title
        self.creator = creator
        # self.tasks = []
        # self.members = []

    def create_task(self, title, description):
        task = Task(title, description, None)
        # self.tasks.append(task)
        dic = load_data()
        dic["tasks"].append(task.title)
        dic["taskdiscription"].append(task.description)
        save_data(dic)#fghjklkjhghjkl;

    def assign_task(self, title, assigned_to):
        dic = load_data()
        for task in dic["tasks"]:
            if task == title:
                dic["taskassigne"].append(assigned_to)
                save_data(dic)
                # Assuming 'assigned_to' is a username, find or create the User object
                member = next((m for m in dic["members"] if m == assigned_to), None)
                if not member:
                    member = User(assigned_to, None)  # Replace None with actual password if available
                    # self.members.append(member)
                return True
        return False#dtylk;kljghk

    def modify_task(self, title=None, description=None, assigned_to=None):
        for task in self.tasks:
            if task.title == title:
                if description:
                    task.description = description
                if assigned_to:
                    task.assigned_to = assigned_to
                return True
        return False

    def add_member(self, username):
        # Create a new User object and add to members list
        member = User(username, None)  # Replace None with actual password if available
        # self.members.append(member)
        dic = load_data()
        dic["members"].append(member)
        save_data(dic)#dfghjkjhgfdfghj
        
    def view_members(self):
        dic = load_data()
        if len(dic["members"]) == 0:
            print("No users yet\n")
        else:
            for member in dic["members"]:
                print(f"\nMembers:\n{member.username}\n")

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.is_activate = True
        # self.projects = []

    def create_project(self, title):
        project = Project(title, self.username)
        # self.projects.append(project)
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
    if login(email) == 1:
        console.print("[bold blue]This account already exists.[/bold blue]\n")
        return None
    username = Prompt.ask("Enter your username:")
    password = Prompt.ask("Enter your password:")
    if email.endswith(".com") and '@' in email and len(password) >= 5:
        console.print("[bold green]Login successful![/bold green]")
        with open("manba.txt", "a") as f:
            f.write(email)
            f.write(" ")
            f.write(username)
            f.write(" ")
            f.write(hashh(password))
            f.write(" ")
            f.write("T")
            f.write(" \n")
        with open("manage.txt", "a") as file:
            file.write("Tedad_Vorood_Movaffaq ")
            file.write(email)
            file.write(" \n")
            
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
            new_content =  content[:number_start] + " 1" + content[number_end:]
        else:
            number = int(content[number_start:number_end]) + 1
            new_content = content[:number_start] + str(number) + content[number_end:]
        
        # Move the file cursor to the beginning and write the new content
        file.seek(0)
        
        file.write(new_content)
        file.truncate()

def increment_number_in_file(name, filepath):
    # Read the file and store its lines
    with open(filepath, 'r') as file:
        lines = file.readlines()

    # Iterate through the lines to find the name and increment the last number
    for i in range(len(lines)):
        if name in lines[i]:
            # Split the line by spaces
            parts = lines[i].split()
            # Check if the line has at least two parts (name and a number)
            if len(parts) >= 2:
                try:
                    # Find the last number in the line
                    last_number = int(parts[-1])
                    # Increment the last number
                    parts[-1] = str(last_number + 1)
                    # Join the parts back together
                    lines[i] = ' '.join(parts) + '\n'
                except ValueError:
                    # If the last part cannot be converted to an integer, skip this line
                    pass

    # Write the modified lines back to the file
    with open(filepath, 'w') as file:
        file.writelines(lines)



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

def check_admin(username , passw):
    a = 0
    with open ("adminfile.txt" , "r") as file:
        content = file.read()
        if (username and passw) in content:
            a = 1
        
    return a
    
    

def display_user_page(user):
    console = Console()
    print(fontstyle.apply(f"Well come {user.username}", 'bold/italic/green'))
    while True:
            choice = Prompt.ask("\nSelect an option:\n1. Create Project\n2. View Projects\n3. View Other User\n4. Exit\n")
            if choice == "1":
                title = Prompt.ask("Enter project title:")
                user.create_project(title)
                console.print("[bold green]Project created successfully![/bold green]")
            elif choice == "2":
                dic = add_project()
                if not user.username in dic.keys():
                    console.print("[bold yellow]You have no projects yet.[/bold yellow]")
                else:
                    table = Table(title="Your Projects")
                    table.add_column("Name", style="cyan", no_wrap=True)
                    table.add_column("Description", style="magenta")
                    for i in dic:
                        if i==user.username:
                            for j in range(len(dic[i])):
                                table.add_row(f"{dic[i][j]}", "rr")
                    console.print(table)
                        # Added logic to view and add members
                    # for project in dic.values():
                    #     ch = Prompt.ask("\n1.View Members\n2.Add Member")
                    #     if ch == '1':
                    #         project.view_members()
                    #     elif ch == '2':
                    #         username_to_add = Prompt.ask("Enter username to add:")
                    #         if username_to_add in project:
                    #             print("Already exist\n")
                    #         else:
                    #             project.add_member(username_to_add)
                    #             console.print("[bold green]Member added successfully![/bold green]")
            elif choice == "3":
                username_to_view = Prompt.ask("Enter username of the user you want to view:")
                console.print(f"[bold blue]Viewing profile of user: {username_to_view}[/bold blue]")
            elif choice == "4":
                break
            else:
                console.print("[bold red]Invalid choice. Please select a valid option.[/bold red]")
def Namovvafaq(filename, target_word):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
        
        with open(filename, "w") as file:
            for line in lines:
                if target_word in line and "vorood_Na_Movaffaq" not in line:
                    line = line.strip() + " vorood_Na_Movaffaq\n"
                file.write(line)
      
    except FileNotFoundError:
        print(f"File '{filename}' not found.")

# Example usage:

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
            user = create_acc()
            if user:
                display_user_page(user)
        elif choice == "2" :
            nam= Prompt.ask("enter your email or username\n")
            ramz = Prompt.ask("Enter Your Pass:\n")
            
            if check_admin(nam , ramz ):
                print("meow")
               
            elif check_pass(nam, hashh(ramz), "manba.txt"):
                tedad_vorood(nam , "manage.txt")
                Namovvafaq("manage.txt" ,nam)
                console.print("[bold green]log in sucsusfully![/bold green]\n")
                user = login_acc(nam, ramz)
                display_user_page(user) 
            elif not check_pass(nam, ramz, "manba.txt"):# and login(nam):
                increment_number_in_file(nam ,"manage.txt")
                x+=1
                console.print(f"[bold red]Wrong username, email or password!![/bold red]\n[yellow]attemp {x} of 4[/yellow]\n")
                if x == 4:
                    console.print("[bold red]try again later[/bold red]")
                    exit()
                    
        elif choice == "3":
            console.print("[bold red]Goodbye![/bold red]")
            exit()
        else:
            x+=1
            console.print("[bold red]Invalid choice. Please select a valid option.[/bold red]\n[yellow]attemp {x} of 4[/yellow]\n")
            if x == 4:
                console.print("[bold red]try again later[/bold red]")
                exit()


if __name__ == "__main__":
    main()