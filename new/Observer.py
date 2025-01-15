import hashlib
import csv
from Logger import Logger

class Observer:
    def update(self, message):
        """Receive update notifications."""
        raise NotImplementedError

class UserNotification(Observer):
    def __init__(self, username):
        self.username = username

    def update(self, message):
        print(f"Notification for {self.username}: {message}")
