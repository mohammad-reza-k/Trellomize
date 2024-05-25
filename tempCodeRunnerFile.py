def purge_data():
    confirmation = input("Are you sure you want to purge all data? (yes/no): ")
    if confirmation.lower() == "yes":
        # Open the file in write mode to clear its contents
        files_to_purge = [
            "tasks.json", "projects.json", "members.json", "memberstask.json", 
            "descriptionstask.json", "projects.txt", "tasks.txt", "members.txt", 
            "memberstask.json", "time.txt", "task_detail.txt", "manba.txt"
        ]
        for filename in files_to_purge:
            with open(filename, "w") as file:
                pass
        print("All data has been purged successfully.")
    else:
        print("Operation cancelled.")