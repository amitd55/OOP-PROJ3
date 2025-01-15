import unittest
from classes.Book import Book
from classes.BorrowingManager import BorrowingManager

class TestBorrowingManagerWithPopularity(unittest.TestCase):

    def setUp(self):
        """Set up a mock book and BorrowingManager for testing."""
        self.manager = BorrowingManager()
        self.mock_book = Book(
            title="Test Book",
            author="Author Name",
            is_loaned=False,
            copies=5,
            genre="Fiction",
            year=2021
        )
        self.manager.book_manager.books = [self.mock_book]

    def test_borrow_book_increments_popularity(self):
        """Test borrowing a book increments its popularity count."""
        initial_popularity = self.mock_book.popularity_count
        self.manager.borrow_book("Test Book")
        self.assertEqual(self.mock_book.popularity_count, initial_popularity + 1)

    def test_return_book_increments_popularity(self):
        """Test returning a book increments its popularity count."""
        self.mock_book.copies_available = 0  # Simulate book being loaned out
        initial_popularity = self.mock_book.popularity_count
        self.manager.return_book("Test Book")
        self.assertEqual(self.mock_book.popularity_count, initial_popularity + 1)

    def test_waiting_list_increments_popularity(self):
        """Test adding a user to the waiting list increments popularity count."""
        self.mock_book.copies_available = 0  # Simulate no copies available
        initial_popularity = self.mock_book.popularity_count
        self.manager.borrow_book("Test Book")  # Should add to waiting list
        self.assertEqual(self.mock_book.popularity_count, initial_popularity + 1)

if __name__ == "__main__":
    unittest.main()
