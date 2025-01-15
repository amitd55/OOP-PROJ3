import unittest
from unittest.mock import MagicMock, patch
from collections import namedtuple
import sys
import os

# Ensure root directory is in PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from GUI.SearchAndDisplayGui import DisplayBooksGui

# Mock book class for testing
MockBook = namedtuple('MockBook', ['title', 'author', 'genre', 'year', 'copies_available'])


class TestDisplayBooksGui(unittest.TestCase):
    def setUp(self):
        """Set up a mocked BookManager and SearchManager."""
        self.mock_books = [
            MockBook("Book A", "Author A", "Fiction", 2020, 5),
            MockBook("Book B", "Author B", "Science", 2019, 0),
            MockBook("Book C", "Author C", "History", 2018, 3),
        ]

        self.mock_book_manager = MagicMock()
        self.mock_book_manager.books = self.mock_books

        self.mock_search_manager = MagicMock()
        self.mock_search_manager.display_books.return_value = iter(self.mock_books)

        with patch("GUI.SearchAndDisplayGui.BookManager", return_value=self.mock_book_manager), \
             patch("GUI.SearchAndDisplayGui.SearchManager", return_value=self.mock_search_manager):
            self.gui = DisplayBooksGui()

    def tearDown(self):
        """Destroy the Tkinter root after each test."""
        self.gui.root.destroy()

    def test_load_books(self):
        """Test loading books into the Treeview."""
        self.gui.load_books()
        # Check that Treeview has the correct number of rows
        tree_items = self.gui.tree.get_children()
        self.assertEqual(len(tree_items), len(self.mock_books))

        # Verify that data matches the mock books
        for i, item in enumerate(tree_items):
            row = self.gui.tree.item(item, 'values')
            self.assertEqual(row[0], self.mock_books[i].title)  # Title
            self.assertEqual(row[1], self.mock_books[i].author)  # Author
            self.assertEqual(row[2], self.mock_books[i].genre)  # Genre
            self.assertEqual(row[3], str(self.mock_books[i].year))  # Year
            self.assertEqual(row[4], str(self.mock_books[i].copies_available))  # Available Copies


if __name__ == "__main__":
    unittest.main()
