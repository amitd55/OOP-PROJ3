import unittest
from unittest.mock import MagicMock
import pandas as pd
from classes.AuthManager import AuthManager

class TestAuthManager(unittest.TestCase):

    def setUp(self):
        # Mock the FileHandler
        self.mock_file_handler = MagicMock()

        # Mock users data as a DataFrame
        self.mock_users_data = pd.DataFrame({
            "username": ["admin"],
            "password_hash": [AuthManager().hash_password("admin123")],
            "role": ["admin"]
        })
        self.mock_file_handler.load_csv.return_value = self.mock_users_data

        # Initialize AuthManager with the mocked FileHandler
        self.auth_manager = AuthManager(file_handler=self.mock_file_handler)

    def test_initialize_default_user(self):
        # Simulate an empty users file
        self.mock_file_handler.load_csv.return_value = pd.DataFrame(columns=["username", "password_hash", "role"])
        self.auth_manager.initialize_default_user()
        self.mock_file_handler.save_csv.assert_called_once()

    def test_register_success(self):
        # Simulate admin logged in
        response = self.auth_manager.register("new_user", "password123", logged_in_user="admin")
        self.assertEqual(response, "Registration successful.")
        self.mock_file_handler.save_csv.assert_called_once()

    def test_register_fail_not_admin(self):
        # Simulate non-admin trying to register
        self.mock_users_data = pd.DataFrame({
            "username": ["admin", "member1"],
            "password_hash": [
                AuthManager().hash_password("admin123"),
                AuthManager().hash_password("pass123")
            ],
            "role": ["admin", "member"]
        })
        self.mock_file_handler.load_csv.return_value = self.mock_users_data

        response = self.auth_manager.register("another_user", "password123", logged_in_user="member1")
        self.assertEqual(response, "Registration failed: Only admins can register new users.")

    def test_register_fail_existing_username(self):
        # Attempt to register a user with an existing username
        response = self.auth_manager.register("admin", "newpassword", logged_in_user="admin")
        self.assertEqual(response, "Registration failed: Username already exists.")

    def test_login_success(self):
        # Test successful login
        response = self.auth_manager.login("admin", "admin123")
        self.assertEqual(response, "Login successful.")

    def test_login_fail_invalid_username(self):
        # Test login with invalid username
        response = self.auth_manager.login("unknown_user", "password123")
        self.assertEqual(response, "Login failed: Invalid username or password.")

    def test_login_fail_invalid_password(self):
        # Test login with invalid password
        response = self.auth_manager.login("admin", "wrongpassword")
        self.assertEqual(response, "Login failed: Invalid username or password.")

if __name__ == "__main__":
    unittest.main()
