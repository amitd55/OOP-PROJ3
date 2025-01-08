from re import search

from Book import Book
from FileManagement import FileManagement
from SearchStrategy import SearchStrategy

class BookCollection:
    def __init__(self):
        self.books=[]

    def __iter__(self):
        return iter(self.books)

    def find_book(self,name):
        for book in self.books:
            if book.name == name:
                return book

    def search(self,strategy):
        results=strategy.search(self.books)
        return BaseBookIterator(results)

    def add_book(self, name, author, year, copies, genre):
        for book in self.books:
            if book.name == name:
                book.update_copies(1)
                FileManagement.update_csv('Books.csv','name',"copies",book.copies)
                return
        new_book = Book(name, author, year, copies, genre)
        self.books.append(new_book)
        FileManagement.append_file('Book.csv',new_book.__str__())

    def delete_book(self,name):
        book = self.find_book(name)
        if not book:
            print(f"Book '{name}' not found in the collection.")
            return
        if book.copies-1==0:
            FileManagement.delete_row('Books.csv','name',book.name)
        else:
            book.copies-=1
            FileManagement.update_csv('Books.csv','name',book.name,'copies',book.copies)





class BaseBookIterator:
    def __init__(self,items):
        self.items=items
        self.index=0


    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.items):
            item=self.items[self.index]
            self.index+=1
            return item
        raise StopIteration

