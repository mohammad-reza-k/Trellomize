import argparse
import os

def create_admin(username, password):
    # Logic to create admin user
    print(f"Creating admin user with username: {username} and password: {password}")

def main():
    parser = argparse.ArgumentParser(description="Script to manage system modes")
    parser.add_argument("command", choices=["create-admin"], help="Command to execute")
    parser.add_argument("--username", help="Username for admin user")
    parser.add_argument("--password", help="Password for admin user")
    
    args = parser.parse_args()

    if args.command == "create-admin":
        if not (args.username and args.password):
            parser.error("Username and password are required for create-admin command")
        create_admin(args.username, args.password)
        
        # Check if mode info file exists
        mode_info_file = "Fa_Haile_Rouge_Mode_Info.txt"
        if os.path.exists(mode_info_file):
            print("Mode information file already exists.")
        else:
            # Create mode info file
            with open(mode_info_file, "w") as file:
                file.write("Mode information of the system")
                
def activate_account(user, command):
    if command=="activate":
        user.is_active = True
        print(f"Account for {user.username} has been activated.")
    else:
        with open("manba.txt", 'r') as file:
            lines = file.readlines()
            new_lines = []
            for line in lines:
                elements = line.split()
                if len(elements) >= 4:
                    if elements[0]==user:
                        elements[3] = 'F'  # Replace 'new_value' with the desired value
                        new_line = ' '.join(elements)
                        new_lines.append(new_line)
                    else:
                        new_lines.append(line)
        with open('manba.txt', 'w') as file:
            for line in new_lines:
                file.write(f"{line}\n")
        
        user.is_activate = False
    
def eliminate():
    # Open the file in write mode to empty its contents
    with open('projects.txt', 'w'):
        pass
    with open('manba.txt', 'w'):
        pass

if __name__ == "__main__":
    main()