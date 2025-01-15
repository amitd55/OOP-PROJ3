import unittest
from classes.BorrowingManager import BorrowingManager
from classes.WaitingListManager import WaitingListManager
from classes.Book import Book

class TestBorrowingManagerWithWaitingList(unittest.TestCase):

    def setUp(self):
        """Set up a BorrowingManager and a mock book for testing."""
        self.borrowing_manager = BorrowingManager()
        self.mock_book = Book("Test Book", "Author", False, 2, "Fiction", 2022)
        self.borrowing_manager.book_manager.books = [self.mock_book]

    def test_borrow_book_available(self):
        """Test borrowing a book with available copies."""
        result = self.borrowing_manager.borrow_book("Test Book")
        self.assertTrue(result)
        self.assertEqual(self.mock_book.copies_available, 1)
        self.assertEqual(self.mock_book.loaned_count, 1)

    def test_borrow_book_unavailable(self):
        """Test borrowing a book when no copies are available."""
        self.mock_book.copies_available = 0
        result = self.borrowing_manager.borrow_book("Test Book")
        self.assertTrue(result)
        self.assertIn("anonymous", self.mock_book.waiting_list_manager.get_waiting_list())

    def test_return_book_with_waiting_list(self):
        """Test returning a book when there's a waiting list."""
        self.mock_book.copies_available = 0
        self.mock_book.waiting_list_manager.add_to_waiting_list("user1")
        result = self.borrowing_manager.return_book("Test Book")
        self.assertTrue(result)
        self.assertEqual(self.mock_book.copies_available, 1)
        self.assertNotIn("user1", self.mock_book.waiting_list_manager.get_waiting_list())

    def test_clear_waiting_list(self):
        """Test clearing the waiting list."""
        self.mock_book.waiting_list_manager.add_to_waiting_list("user1")
        self.mock_book.waiting_list_manager.add_to_waiting_list("user2")
        self.mock_book.waiting_list_manager.clear_waiting_list()
        self.assertEqual(len(self.mock_book.waiting_list_manager.get_waiting_list()), 0)

if __name__ == "__main__":
    unittest.main()
