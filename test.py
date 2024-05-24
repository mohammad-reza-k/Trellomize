import os
import pytest
from manager import create_admin, activate_account, purge_data

@pytest.fixture
def admin_file_path(tmp_path):
    return tmp_path / "adminfile.txt"

@pytest.fixture
def user_account_file(tmp_path):
    return tmp_path / "manba.txt"

def test_create_admin(admin_file_path):
    username = "admin"
    password = "adminpass"
    create_admin(username, password)
    assert os.path.exists(admin_file_path)

def test_activate_account(user_account_file):
    # Prepare test data
    user = "testuser"
    command = "activate"
    with open(user_account_file, "w") as file:
        file.write("someuser somepassword F\n")
        file.write(f"{user} somepassword F\n")
        file.write("anotheruser anotherpassword F\n")

    # Test account activation
    activate_account(user, command)
    with open(user_account_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            if user in line:
                assert line.strip().endswith("T")

def test_deactivate_account(user_account_file):
    # Prepare test data
    user = "testuser"
    command = "deactivate"
    with open(user_account_file, "w") as file:
        file.write("someuser somepassword T\n")
        file.write(f"{user} somepassword T\n")
        file.write("anotheruser anotherpassword T\n")

    # Test account deactivation
    activate_account(user, command)
    with open(user_account_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            if user in line:
                assert line.strip().endswith("F")

def test_purge_data(tmp_path):
    # Prepare test data
    files_to_check = [
        "tasks.json", "projects.json", "members.json", "memberstask.json", 
        "descriptionstask.json", "projects.txt", "tasks.txt", "members.txt", 
        "memberstask.json", "time.txt", "task_detail.txt", "manba.txt"
    ]
    for filename in files_to_check:
        filepath = tmp_path / filename
        with open(filepath, "w") as file:
            file.write("test data")

    # Test data purging
    purge_data()
    for filename in files_to_check:
        filepath = tmp_path / filename
        assert not os.path.exists(filepath)
