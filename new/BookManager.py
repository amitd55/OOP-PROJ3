from FileHandler import FileHandler
from Book import Book
from Logger import Logger
import pandas as pd

class BookManager:
    def __init__(self):
        self.file_handler = FileHandler()
        self.logger = Logger()
        self.books = self.load_books()

    def load_books(self):
        """Load books from the master file."""
        try:
            books_data = self.file_handler.load_csv("books.csv")
            if books_data.empty:
                self.logger.log_action("books.csv exists but contains no data. Books list remains empty.")
                return []

            self.logger.log_action(f"Loaded {len(books_data)} books from books.csv.")
            return [
                Book(
                    title=row["title"],
                    author=row["author"],
                    is_loaned=(row["is_loaned"].strip().lower() == "yes"),
                    copies=int(row["copies"]),
                    genre=row["genre"],
                    year=int(row["year"])
                ) for _, row in books_data.iterrows()
            ]
        except FileNotFoundError:
            self.logger.log_action("books.csv not found. Initializing a new file on save.")
            return []
        except Exception as e:
            self.logger.log_action(f"Unexpected error loading books: {e}")
            return []

    def save_books(self):
        """Save all books and synchronize files."""
        try:
            if not self.books:
                self.logger.log_action("No books available to save. Skipping save operation.")
                return

            all_books_df = pd.DataFrame([book.to_dict() for book in self.books])
            loaned_books_df = all_books_df[all_books_df["copies_available"] == 0]
            available_books_df = all_books_df[all_books_df["copies_available"] > 0]

            self.file_handler.save_csv("books.csv", all_books_df)
            self.file_handler.save_csv("loaned_books.csv", loaned_books_df)
            self.file_handler.save_csv("available_books.csv", available_books_df)

            self.logger.log_action("Books saved successfully to all files.")
        except Exception as e:
            self.logger.log_action(f"Error saving books: {e}")

    @Logger().log_action
    def add_book(self, title, author, genre, year, copies):
        """Add a new book or update an existing book."""
        try:
            book = next((b for b in self.books if b.title == title and b.author == author), None)

            if book:
                book.copies += copies
                book.copies_available += copies
                book.is_loaned = book.copies_available == 0
                message = "Book updated with additional copies."
            else:
                new_book = Book(title, author, False, copies, genre, year)
                self.books.append(new_book)
                message = "New book added successfully."

            self.save_books()
            return {"action": "add book", "success": True, "message": message}
        except Exception as e:
            self.logger.log_action(f"Error adding book: {e}")
            return {"action": "add book", "success": False, "message": f"Error adding book: {e}"}

    @Logger().log_action
    def remove_book(self, title):
        """Remove a book by title."""
        try:
            self.books = [book for book in self.books if book.title != title]
            self.save_books()
            return {"action": "book removed", "success": True, "message": "Book removed successfully."}
        except Exception as e:
            self.logger.log_action(f"Error removing book: {e}")
            return {"action": "book removed", "success": False, "message": f"Error: {e}"}

    @Logger().log_action
    def get_popular_books(self, min_requests=10):
        """Retrieve popular books based on request count."""
        try:
            return [book for book in self.books if book.get_request_metric() >= min_requests]
        except Exception as e:
            self.logger.log_action(f"Error retrieving popular books: {e}")
            raise

    @Logger().log_action
    def get_books_by_genre(self, genre):
        """Retrieve books by genre."""
        try:
            return [book for book in self.books if book.genre.lower() == genre.lower()]
        except Exception as e:
            self.logger.log_action(f"Error retrieving books by genre: {e}")
            raise
