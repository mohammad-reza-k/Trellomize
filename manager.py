import argparse
import os
from rich.console import Console

def create_admin(username, password):
    # Check if adminfile already exists
    mode_info_file = "adminfile.txt"
    if os.path.exists(mode_info_file):
        print("The system mode is already built.")
        return

    # Logic to create admin user
    print(f"Creating admin user with username: {username} and password: {password}")
    with open(mode_info_file, "w") as file:
        file.write(username)
        file.write(" ")
        file.write(password)
    print(f"Admin user information written to {mode_info_file}")

def activate_account(user, command):
    if command == "activate":
        # user.is_active = True
        with open("manba.txt", 'r') as file:
            lines = file.readlines()
            new_lines = []
            for line in lines:
                elements=line.split()
                if elements[1]==user or elements[0]==user:
                    elements[3]='T'
                    new_lines=' '.join(elements)
                    elements.append(new_lines)
                    
        with open('manba.txt', 'w') as file:
            for line in new_lines:
                file.write(f"{line}\n")

        print(f"Account for {user} has been activated.")
    elif command == "deactivate":
        with open("manba.txt", 'r') as file:
            lines = file.readlines()
            new_lines = []
            for line in lines:
                elements = line.split()
                if len(elements) >= 4:
                    if elements[1] == user or elements[0] == user:
                        elements[3] = 'F'  # Replace 'new_value' with the desired value
                        new_line = ' '.join(elements)
                        new_lines.append(new_line)
                    else:
                        new_lines.append(line)
        with open('manba.txt', 'w') as file:
            for line in new_lines:
                file.write(f"{line}\n")
        print(f"Account for {user} has been deactivated.")

def purge_data():
        console = Console()
        con = input("Are you sure you want to pureg all data? (yes/no)")
        if con.lower()=='no':
            console.print("[bold yellow]Operation canceled[/bold yellow]")
        elif con.lower()=='yes':
            files_to_purge = [
                "tasks.json", "projects.json", "members.json", "memberstask.json", 
                "descriptionstask.json", "projects.txt", "tasks.txt", "members.txt", 
                "memberstask.txt", "time.txt", "task_details.txt", "manba.txt", "time.json", "prio.json", 
                "manage.txt"
                
            ]
            for filename in files_to_purge:
                with open(filename, "w") as file:
                    pass
            console.print("[bold yellow]All data has been purged successfully[/bold yellow]")
        else:
            console.print("[bold red]Kerm nariz da[bold red]")
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage system modes")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Create admin command
    create_admin_parser = subparsers.add_parser("create-admin", help="Create an admin user")
    create_admin_parser.add_argument("--username", required=True, help="Username for admin user")
    create_admin_parser.add_argument("--password", required=True, help="Password for admin user")

    # Purge data command
    purge_data_parser = subparsers.add_parser("purge-data", help="Purge data from the system")

    args = parser.parse_args()

    if args.command == "create-admin":
        create_admin(args.username, args.password)
    elif args.command == "purge-data":
        purge_data()
    else:
        parser.print_help()