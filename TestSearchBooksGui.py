import unittest
from unittest.mock import MagicMock, patch
from collections import namedtuple
from GUI.SearchAndDisplayGui import SearchBooksGui

# Mock Book class
MockBook = namedtuple("MockBook", ["title", "author", "genre", "year", "copies_available"])


class TestSearchBooksGui(unittest.TestCase):
    def setUp(self):
        """Set up a mocked SearchBooksGui with a mocked SearchManager."""
        # Mock books for testing
        self.mock_books = [
            MockBook("Book A", "Author A", "Fiction", 2020, 5),
            MockBook("Book B", "Author B", "Science", 2019, 0),
            MockBook("Book C", "Author C", "History", 2018, 3),
        ]

        # Mock BookManager
        self.mock_book_manager = MagicMock()
        self.mock_book_manager.books = self.mock_books

        # Mock SearchManager
        self.mock_search_manager = MagicMock()
        self.mock_search_manager.perform_search.side_effect = self.mock_search_logic

        # Patch dependencies in SearchBooksGui
        with patch("GUI.SearchAndDisplayGui.BookManager", return_value=self.mock_book_manager), \
             patch("GUI.SearchAndDisplayGui.SearchManager", return_value=self.mock_search_manager):
            self.gui = SearchBooksGui()

        # Replace the GUI's SearchManager with the mock
        self.gui.search_manager = self.mock_search_manager

    def mock_search_logic(self, query, search_type):
        """Simulate search logic."""
        if search_type == "title":
            return [book for book in self.mock_books if query.lower() in book.title.lower()]
        elif search_type == "author":
            return [book for book in self.mock_books if query.lower() in book.author.lower()]
        elif search_type == "genre":
            return [book for book in self.mock_books if query.lower() in book.genre.lower()]
        elif search_type == "year":
            return [book for book in self.mock_books if str(query) == str(book.year)]
        else:
            raise ValueError(f"Invalid search type: {search_type}")

    def tearDown(self):
        """Destroy Tk root after each test."""
        self.gui.root.destroy()

    def test_books_loaded(self):
        """Test if books are loaded correctly in BookManager."""
        self.assertEqual(len(self.mock_book_manager.books), 3)  # Assert books are loaded
        self.assertEqual(self.mock_book_manager.books[0].title, "Book A")  # Check a specific book

    def test_search_results_found(self):
        """Test searching by title with matching results."""
        self.gui.search_query_entry.insert(0, "Book A")  # Simulate user input
        self.gui.search_type_var.set("title")  # Simulate radio button selection

        self.gui.perform_search()

        # Verify SearchManager was called correctly
        self.mock_search_manager.perform_search.assert_called_once_with("Book A", "title")

        # Verify Treeview was updated
        tree_items = self.gui.tree.get_children()
        self.assertEqual(len(tree_items), 1)  # Only one match
        row = self.gui.tree.item(tree_items[0], "values")
        self.assertEqual(row[0], "Book A")  # Check title in Treeview

    def test_search_no_results(self):
        """Test searching with no matching results."""
        self.gui.search_query_entry.insert(0, "Nonexistent")
        self.gui.search_type_var.set("title")

        self.gui.perform_search()

        # Verify SearchManager was called correctly
        self.mock_search_manager.perform_search.assert_called_once_with("Nonexistent", "title")

        # Verify Treeview has no items
        tree_items = self.gui.tree.get_children()
        self.assertEqual(len(tree_items), 0)  # No matches

    def test_invalid_search_type(self):
        """Test searching with an invalid search type."""
        self.gui.search_query_entry.insert(0, "Some Query")
        self.gui.search_type_var.set("invalid_type")  # Simulate invalid type

        with patch("tkinter.messagebox.showerror") as mock_messagebox:
            self.gui.perform_search()
            mock_messagebox.assert_called_once_with("Error", "Search failed: Invalid search type: invalid_type")

        self.mock_search_manager.perform_search.assert_not_called()  # Ensure perform_search was not called

    def test_empty_query(self):
        """Test searching with an empty query."""
        self.gui.search_query_entry.delete(0, "end")  # Ensure query is empty
        self.gui.search_type_var.set("title")

        with patch("tkinter.messagebox.showerror") as mock_messagebox:
            self.gui.perform_search()
            mock_messagebox.assert_called_once_with("Error", "Please enter a query.")

        self.mock_search_manager.perform_search.assert_not_called()


if __name__ == "__main__":
    unittest.main()
