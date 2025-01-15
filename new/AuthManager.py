from FileHandler import FileHandler
import hashlib


class AuthManager:
    def __init__(self, file_handler=None, user_file="users.csv"):
        self.file_handler = file_handler or FileHandler()  # Use provided FileHandler or create a new one
        self.user_file = user_file
        self.initialize_default_user()  # Ensure the default admin user exists

    def hash_password(self, password):
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def initialize_default_user(self):
        """Ensure a default admin user exists."""
        users = self.load_users()
        if users.empty:  # No users found
            default_user = {
                "username": "admin",
                "password_hash": self.hash_password("admin123"),
                "role": "admin"
            }
            self.file_handler.save_csv(self.user_file, [default_user], fieldnames=["username", "password_hash", "role"])
            print("Default admin user created: Username: 'admin', Password: 'admin123'")

    def register(self, username, password, logged_in_user):
        """Register a new user."""
        users = self.load_users()

        # Only admins can register new users
        if logged_in_user not in users["username"].values or \
                users.loc[users["username"] == logged_in_user, "role"].iloc[0] != "admin":
            return "Registration failed: Only admins can register new users."

        if username in users["username"].values:
            return "Registration failed: Username already exists."

        new_user = {
            "username": username,
            "password_hash": self.hash_password(password),
            "role": "member"  # Default role is member
        }
        self.file_handler.save_csv(self.user_file, [new_user], fieldnames=["username", "password_hash", "role"])
        return "Registration successful."

    def login(self, username, password):
        """Log in an existing user."""
        users = self.load_users()
        if username in users["username"].values:
            hashed_password = self.hash_password(password)
            stored_password = users.loc[users["username"] == username, "password_hash"].iloc[0]
            if hashed_password == stored_password:
                return "Login successful."
        return "Login failed: Invalid username or password."

    def load_users(self):
        """Load users from the CSV file into a DataFrame."""
        return self.file_handler.load_csv(self.user_file)
