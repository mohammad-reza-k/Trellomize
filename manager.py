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
        mode_info_file = "adminfile.txt"
        with open(mode_info_file, "w") as file:
            file.write(args.username)
            file.write(" ")
            file.write(args.password)
                
def activate_account(user, command):
    if command=="activate":
        # user.is_active = True
        with open("manba.txt", 'r') as file:
            lines = file.readlines()
            new_lines = []
            for line in lines:
                elements = line.split()
                if len(elements) >= 4:
                    if elements[1]==user or elements[0]==user:
                        elements[3] = 'T'  # Replace 'new_value' with the desired value
                        new_line = ' '.join(elements)
                        new_lines.append(new_line)
                    else:
                        new_lines.append(line)
        with open('manba.txt', 'w') as file:
            for line in new_lines:
                file.write(f"{line}\n")

        print(f"Account for {user} has been activated.")
    elif command=="diactivate":
        with open("manba.txt", 'r') as file:
            lines = file.readlines()
            new_lines = []
            for line in lines:
                elements = line.split()
                if len(elements) >= 4:
                    if elements[1]==user or elements[0]==user:
                        elements[3] = 'F'  # Replace 'new_value' with the desired value
                        new_line = ' '.join(elements)
                        new_lines.append(new_line)
                    else:
                        new_lines.append(line)
        with open('manba.txt', 'w') as file:
            for line in new_lines:
                file.write(f"{line}\n")
        print(f"Account for {user} has been diactivated.")

        #user.is_activate = False



def purge_data():
    confirmation = input("Are you sure you want to purge all data? (yes/no): ")
    if confirmation.lower() == "yes":
        # Open the file in write mode to clear its contents
        with open("manba.txt", "w") as f:
            pass  
        
        with open("projects.txt" ,"w") as fi:
            pass
        with open("members.json" ,"w") as p:
            pass
        with open ("members.txt" , "w") as d:
            pass
        with open ("tasks.json" , "w") as g:
            pass
        
        print("All data has been purged successfully.")
         
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Purge data from the system.")
    parser.add_argument("action", choices=["purge-data"], help="Action to perform")
    args = parser.parse_args()

    if args.action == "purge-data":
        purge_data()
    else:
        print("Invalid action. Please specify 'purge-data'.")
    
