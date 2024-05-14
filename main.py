from rich.prompt import Prompt
from rich.console import Console

class Task:
    def __init__(self, task_id, title, description, assigned_to):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.assigned_to = assigned_to

class Project:
    def __init__(self, project_id, title, creator):
        self.project_id = project_id
        self.title = title
        self.creator = creator
        self.tasks = []
        self.members = []

    def create_task(self, task_id, title, description):
        task = Task(task_id, title, description, None)
        self.tasks.append(task)

    def assign_task(self, task_id, assigned_to):
        for task in self.tasks:
            if task.task_id == task_id:
                task.assigned_to = assigned_to
                # Assuming 'assigned_to' is a username, find or create the User object
                member = next((m for m in self.members if m.username == assigned_to), None)
                if not member:
                    member = User(assigned_to, None)  # Replace None with actual password if available
                    self.members.append(member)
                return True
        return False

    def modify_task(self, task_id, title=None, description=None, assigned_to=None):
        for task in self.tasks:
            if task.task_id == task_id:
                if title:
                    task.title = title
                if description:
                    task.description = description
                if assigned_to:
                    task.assigned_to = assigned_to
                return True
        return False

    def add_member(self, username):
        # Create a new User object and add to members list
        member = User(username, None)  # Replace None with actual password if available
        self.members.append(member)

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

    def create_project(self, project_id, title):
        project = Project(project_id, title, self.username)
        self.projects.append(project)

def login():
    console = Console()
    email = Prompt.ask("Enter your email:")
    username = Prompt.ask("Enter your username:")
    password = Prompt.ask("Enter your password:", password=True)
    if email.endswith(".com") and '@' in email and username[0].isupper() and len(password) >= 5:
        console.print("[bold green]Login successful![/bold green]")
        return User(username, password)
    else:
        console.print("[bold red]Invalid email, username, or password. Please try again.[/bold red]")
        return None

def display_user_page(user):
    console = Console()
    console.print(f"Welcome, {user.username}!")
    while True:
        choice = Prompt.ask("\nSelect an option:\n1. Create Project\n2. View Projects\n3. View Other User\n4. Exit\n")
        if choice == "1":
            project_id = Prompt.ask("Enter project ID:")
            title = Prompt.ask("Enter project title:")
            user.create_project(project_id, title)
            console.print("[bold green]Project created successfully![/bold green]")
        elif choice == "2":
            if not user.projects:
                console.print("[bold yellow]You have no projects yet.[/bold yellow]")
            else:
                console.print("[bold blue]Your Projects:[/bold blue]")
                for project in user.projects:
                    console.print(f"Project ID: {project.project_id}, Title: {project.title}, Creator: {project.creator}")
                    project.add_member(user.username)
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

def main():
    user = login()
    if user:
        display_user_page(user)

if __name__ == "__main__":
    main()
