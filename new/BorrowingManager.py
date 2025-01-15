from Logger import Logger
from BookManager import BookManager

class BorrowingManager(BookManager):
    # def __init__(self):
    #     self.book_manager = BookManager()
    #     self.logger = Logger()

    @Logger().log_action
    def borrow_book(self, title, username):
        try:
            book = next((b for b in self.books if b.title == title), None)

            if not book:
                return {"action": "borrow book", "success": False, "message": "Book not found"}

            if book.copies_available > 0:
                book.copies_available -= 1
                book.loaned_count += 1
                if book.copies_available == 0:
                    book.is_loaned = True
                self.save_books()
                return {"action": "borrow book", "success": True, "message": "Book borrowed successfully"}
            else:
                book.add_to_waiting_list(username)
                self.save_books()
                return {"action": "borrow book", "success": True, "message": "Book unavailable; added to waiting list"}
        except Exception as e:
            print(f"Error borrowing book: {e}")
            return {"action": "borrow book", "success": False}

    @Logger().log_action
    def return_book(self, title, username):
        try:
            book = next((b for b in self.books if b.title == title), None)

            if not book:
                return {"action": "return book", "success": False, "message": "Book not found"}

            book.copies_available += 1
            if book.copies_available == book.copies:
                book.is_loaned = False

            next_user = book.remove_from_waiting_list()
            self.save_books()
            if next_user:
                return {"action": "return book", "success": True, "message": f"Book returned; notified {next_user}"}
            return {"action": "return book", "success": True, "message": "Book returned successfully"}
        except Exception as e:
            print(f"Error returning book: {e}")
            return {"action": "return book", "success": False}

