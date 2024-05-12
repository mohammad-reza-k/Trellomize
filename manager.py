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

if __name__ == "__main__":
    main()
