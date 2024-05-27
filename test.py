import unittest
from manager import activate_account, purge_data
import main
from datetime import datetime
from io import StringIO
import os
from main import today_date , time
from manager import create_admin
from unittest.mock import mock_open, patch
from manager import purge_data
from main import log_system_event ,log_file_operation , log_user_action_del
from main import add_project
from main import login
from main import check_pass

class TestActivateAccountFunction(unittest.TestCase):
    def setUp(self):
        # Create a test file with initial user data
        with open("manba.txt", "w") as file:
            file.write("user1 email1@example.com password1 F\n")
            file.write("user2 email2@example.com password2 T\n")
            file.write("user3 email3@example.com password3 F\n")

    def tearDown(self):
        # Remove the test file after the test
        
        os.remove("manba.txt")

    def test_activate_account(self):
        # Arrange
        user = "user1"
        command = "activate"

        # Act
        activate_account(user, command)

        # Assert
        with open("manba.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                elements = line.split()
                if len(elements) >= 4 and (elements[0] == user or elements[1] == user):
                    self.assertEqual(elements[3], 'T')
                    break
            else:
                self.fail("User not found or account not activated.")

    def test_deactivate_account(self):
        # Arrange
        user = "user2"
        command = "deactivate"

        # Act
        activate_account(user, command)

        # Assert
        with open("manba.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                elements = line.split()
                if len(elements) >= 4 and (elements[0] == user or elements[1] == user):
                    self.assertEqual(elements[3], 'F')
                    break
            else:
                self.fail("User not found or account not deactivated.")
                
class TestCreateAdmin(unittest.TestCase):

    def setUp(self):
        # Ensure adminfile.txt does not exist before each test
        if os.path.exists("adminfile.txt"):
            os.remove("adminfile.txt")

    def test_create_admin_success(self):
        create_admin("admin", "password")
        self.assertTrue(os.path.exists("adminfile.txt"))

    def test_create_admin_file_exists(self):
        # Create a dummy adminfile.txt to simulate existing admin file
        with open("adminfile.txt", "w") as file:
            file.write("dummy_admin dummy_password")
        create_admin("admin", "password")
        self.assertTrue(os.path.exists("adminfile.txt"))

class TestPurgeData(unittest.TestCase):

    @patch('builtins.input', return_value="yes")
    @patch('sys.stdout', new_callable=StringIO)
    def test_purge_data_confirmation_yes(self, mock_stdout, mock_input):
        purge_data()
        for filename in [
            "tasks.json", "projects.json", "members.json", "memberstask.json", 
            "descriptionstask.json", "projects.txt", "tasks.txt", "members.txt", 
            "memberstask.json", "time.txt", "task_detail.txt", "manba.txt"
        ]:
            self.assertTrue(os.path.isfile(filename))
        self.assertIn("All data has been purged successfully.", mock_stdout.getvalue())

    @patch('builtins.input', return_value="no")
    @patch('sys.stdout', new_callable=StringIO)
    def test_purge_data_confirmation_no(self, mock_stdout, mock_input):
        purge_data()
        for filename in [
            "tasks.json", "projects.json", "members.json", "memberstask.json", 
            "descriptionstask.json", "projects.txt", "tasks.txt", "members.txt", 
            "memberstask.json", "time.txt", "task_detail.txt", "manba.txt"
        ]:
            self.assertTrue(os.path.isfile(filename))
        self.assertIn("Operation cancelled.", mock_stdout.getvalue())
                
       #main         
class TestDateTimeFunctions(unittest.TestCase):

    def test_today_date(self):
        self.assertEqual(today_date(), datetime.today().date())

    def test_time(self):
        self.assertEqual(time(), datetime.now().time())
class TestLoginFunction(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='email1 user1 pass1 t1\nemail2 user2 pass2 t2\n')
    def test_username_exists(self, mock_file):
        result = login('user1')
        self.assertEqual(result, 1)
    
    @patch('builtins.open', new_callable=mock_open, read_data='email1 user1 pass1 t1\nemail2 user2 pass2 t2\n')
    def test_username_does_not_exist(self, mock_file):
        result = login('user3')
        self.assertEqual(result, 0)
    
    @patch('builtins.open', new_callable=mock_open, read_data='email1 user1 pass1 t1\nemail2 user2 pass2 t2\n')
    def test_file_not_found(self, mock_file):
        mock_file.side_effect = FileNotFoundError
        result = login('user1')
        self.assertEqual(result, 0)

class TestCheckPassFunction(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='email1 user1 pass1 T\nemail2 user2 pass2 F\n')
    def test_valid_user_active(self, mock_file):
        result = check_pass('user1', 'pass1')
        self.assertTrue(result)
    
    @patch('builtins.open', new_callable=mock_open, read_data='email1 user1 pass1 T\nemail2 user2 pass2 F\n')
    def test_valid_user_banned(self, mock_file):
        result = check_pass('user2', 'pass2')
        self.assertFalse(result)

    @patch('builtins.open', new_callable=mock_open, read_data='email1 user1 pass1 T\nemail2 user2 pass2 F\n')
    def test_invalid_password(self, mock_file):
        result = check_pass('user1', 'wrongpass')
        self.assertFalse(result)
    
    @patch('builtins.open', new_callable=mock_open, read_data='email1 user1 pass1 T\nemail2 user2 pass2 F\n')
    def test_user_not_found(self, mock_file):
        result = check_pass('user3', 'pass3')
        self.assertFalse(result)

    @patch('builtins.open', new_callable=mock_open, read_data='email1 user1 pass1\nemail2 user2 pass2\n')  # Invalid format
    def test_invalid_format_in_file(self, mock_file):
        result = check_pass('user1', 'pass1')
        self.assertFalse(result)
    
    @patch('builtins.open', new_callable=mock_open)
    def test_file_not_found(self, mock_file):
        mock_file.side_effect = FileNotFoundError
        result = check_pass('user1', 'pass1')
        self.assertFalse(result)





if __name__ == '__main__':
    unittest.main()