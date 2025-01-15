from classes.BookManager import BookManager
from classes.Logger import Logger


class BorrowingManager:

    def __init__(self):
        self.book_manager = BookManager()

    @Logger().log_action
    def borrow_book(self, title):
        try:
            book = next((b for b in self.book_manager.books if b.title == title), None)
            if not book:
                print(f"Error: Book '{title}' not found.")
                return False

            if book.copies_available > 0:
                book.copies_available -= 1
                book.loaned_count += 1
                book.popularity_count += 1
                if book.copies_available == 0:
                    book.is_loaned = True
                self.book_manager.save_books()
                return True
            else:
                # Add to waiting list without specific username
                book.waiting_list_manager.add_to_waiting_list("anonymous")
                book.popularity_count+=1
                self.book_manager.save_books()
                return True
        except Exception as e:
            print(f"Error borrowing book: {e}")
            return False

    @Logger().log_action
    def return_book(self, title):
        try:
            book = next((b for b in self.book_manager.books if b.title == title), None)

            if not book:
                print(f"Error: Book '{title}' not found.")
                return False

            book.copies_available += 1
            if book.copies_available == book.copies:
                book.is_loaned = False

            next_user = book.waiting_list_manager.remove_from_waiting_list()
            book.popularity_count += 1
            self.book_manager.save_books()

            if next_user:
                print(f"Notified that the book '{title}' is now available.")
                return True
            return True
        except Exception as e:
            print(f"Error returning book: {e}")
            return False
