from BookManager import BookManager
from Logger import Logger

class SearchStrategy:
    def search(self, books, query):
        """Abstract method to perform a search."""
        raise NotImplementedError

class TitleSearchStrategy(SearchStrategy):
    def search(self, books, query):
        return [book for book in books if query.lower() in book.title.lower()]

class AuthorSearchStrategy(SearchStrategy):
    def search(self, books, query):
        return [book for book in books if query.lower() in book.author.lower()]

class GenreSearchStrategy(SearchStrategy):
    def search(self, books, query):
        return [book for book in books if query.lower() in book.genre.lower()]

class SearchManager:
    def __init__(self):
        self.book_manager = BookManager()
        self.logger = Logger()
        self.strategy = None

    def set_strategy(self, strategy):
        """Set the search strategy."""
        self.strategy = strategy

    @Logger().log_action
    def search(self, query):
        """Perform a search using the selected strategy."""
        if not self.strategy:
            self.logger.log("Search failed: No search strategy set.")
            raise ValueError("Search strategy not set.")

        books = self.book_manager.books
        results = self.strategy.search(books, query)

        if results:
            self.logger.log(f"Search '{query}' completed successfully with {len(results)} result(s).")
        else:
            self.logger.log(f"Search '{query}' failed: No matches found.")

        return results

    @Logger().log_action
    def display_books(self, status="all"):
        """Display books based on their loan status."""
        try:
            if status == "available":
                books = [book for book in self.book_manager.books if book.copies_available > 0]
            elif status == "loaned":
                books = [book for book in self.book_manager.books if book.copies_available == 0]
            elif status == "all":
                books = self.book_manager.books
            else:
                raise ValueError("Invalid status. Use 'all', 'available', or 'loaned'.")

            self.logger.log(f"Displayed {status} books successfully with {len(books)} result(s).")
            return books
        except Exception as e:
            self.logger.log(f"Displaying {status} books failed: {e}")
            raise
