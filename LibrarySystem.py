import SearchStrategy
from BookCollection import BookCollection
from FileManagement import FileManagement


class LibrarySystem:
    def __init__(self):
        self.books_collection=BookCollection()


    def borrow_book(self, name):
        book= self.books_collection.find_book(name)
        if book.available_copies()>0:
            book.borrow_book()
            self._update_files_after_action("borrow",book)


    def return_book(self, name):
        book= self.books_collection.find_book(name)
        book.return_book()
        self._update_files_after_action("return",book)

    def add_book(self, name, author, year, copies, genre):
        self.books_collection.add_book(name, author, year, copies, genre)

    def search_books(self, strategy):
        self.books_collection.search(strategy)

    def update_book_copies(self, name: str, additional_copies: int):
        pass


    def _update_files_after_action(self,action,book):
        if action =="borrow":
            FileManagement.append_file('loaned_books.csv', book.__str__())
            if book.available_copies() == 0:
                FileManagement.delete_row('available_books.csv', 'name', book.name)
            else:
                FileManagement.update_csv('available_books.csv', 'name', book.name, 'copies', book.available_copies())

        elif action == "return":
            if book.available_copies() == book.copies:
                FileManagement.delete_row('loaned_books.csv', 'name', book.name)
            FileManagement.update_csv('available_books.csv', 'name', book.name, 'copies', book.available_copies())

        elif action == "add":
            FileManagement.append_file('available_books.csv', book.__str__())

        elif action == "remove":
            FileManagement.delete_row('available_books.csv', 'name', book.name)


