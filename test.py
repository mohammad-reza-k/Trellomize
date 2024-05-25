'''
import unittest
from manager import activate_account, purge_data
import main
from datetime import datetime
from io import StringIO
import os
from main import today_date , time
from manager import create_admin
from unittest.mock import patch

from manager import purge_data
'''
'''
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





'''
import unittest
from unittest.mock import patch
from io import StringIO
import os
from datetime import datetime


from main import log_system_event ,log_file_operation , log_user_action_del
class TestLoggingFunctions(unittest.TestCase):

    def setUp(self):
        # Remove log files before each test
        for filename in ['user_actions.log', 'system_events.log']:
            if os.path.exists(filename):
                os.remove(filename)

    @patch('sys.stdout', new_callable=StringIO)
    def test_log_file_operation(self, mock_stdout):
        log_file_operation('read', 'test_file.txt')
        self.assertTrue(os.path.exists('test_file.txt'))
        self.assertIn('read operation performed on file: test_file.txt', mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_log_user_action(self, mock_stdout):
        log_user_action('user1', 'login')
        self.assertTrue(os.path.exists('user_actions.log'))
        self.assertIn("User 'user1' performed action: login", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_log_user_action_del(self, mock_stdout):
        log_user_action_del('user1', 'task1')
        self.assertTrue(os.path.exists('user_actions.log'))
        self.assertIn("User 'user1' performed action: Deleted task1", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_log_system_event(self, mock_stdout):
        log_system_event('new_project')
        self.assertTrue(os.path.exists('system_events.log'))
        self.assertIn("System event: project :new_project", mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()