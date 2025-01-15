import pandas as pd
from Logger import Logger
from FileHandler import FileHandler
from Observer import Observer

class Book:
    def __init__(self, title, author, is_loaned, copies, genre, year):
        self.title = title
        self.author = author
        self.is_loaned = is_loaned
        self.copies = copies
        self.genre = genre
        self.year = year
        self.loaned_count = self.copies if self.is_loaned else 0
        self.waiting_list = []  # FIFO list for client names
        self.copies_available = 0 if is_loaned else copies
        self.popularity_count= self.loaned_count
        self.observers = []  # List of observers

    # Observer Methods
    def add_observer(self, observer):
        """Add an observer to be notified."""
        self.observers.append(observer)

    def remove_observer(self, observer):
        """Remove an observer."""
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self, message):
        """Notify all observers about an update."""
        for observer in self.observers:
            observer.update(message)

    def add_to_waiting_list(self, username):
        if username not in self.waiting_list:
            self.waiting_list.append(username)
            self.add_observer(Observer(username))

    def remove_from_waiting_list(self):
        if self.waiting_list:
            username = self.waiting_list.pop(0)
            self.notify_observers(f"The book '{self.title}' is now available for {username}.")
            return username
        return None

    def update_details(self, **kwargs):
        """Dynamically update book details."""
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)


    def to_dict(self):
        """Convert the book object to a dictionary for DataFrame compatibility."""
        return {
            "title": self.title,
            "author": self.author,
            "is_loaned": self.is_loaned,
            "copies": self.copies,
            "genre": self.genre,
            "year": self.year,
            "loaned_count": self.loaned_count,
            "waiting_list": ",".join(self.waiting_list),
            "copies_available": self.copies_available,
            "popularity_count":self.popularity_count
        }

    def __str__(self):
        return (f"Title: {self.title}, Author: {self.author}, Year: {self.year}, "
                f"Genre: {self.genre}, Copies: {self.copies}, Loaned: {self.is_loaned}, "
                f"Waiting List: {self.waiting_list}")


