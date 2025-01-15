from BookManager import BookManager
from Logger import Logger

class AnalyticsManager:
    def __init__(self):
        self.book_manager = BookManager()
        self.logger = Logger()

    @Logger().log_action
    def get_top_books(self, top_n=10):
        """Get the top N most popular books based on borrow count and waiting list size."""
        books = self.book_manager.books
        # Calculate popularity score
        for book in books:
            book.popularity_score = book.loaned_count + len(book.waiting_list)

        # Sort by popularity score (descending)
        sorted_books = sorted(books, key=lambda b: b.popularity_score, reverse=True)
        return sorted_books[:top_n]

    @Logger().log_action
    def display_top_books(self, top_n=10):
        """Display the top N most popular books."""
        top_books = self.get_top_books(top_n)
        print(f"Top {top_n} Most Popular Books:")
        for rank, book in enumerate(top_books, start=1):
            print(f"{rank}. {book.title} by {book.author} - Genre: {book.genre}, Popularity Score: {book.popularity_score}")
