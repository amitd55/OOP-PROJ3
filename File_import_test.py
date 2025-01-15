from classes.BookManager import BookManager

# Create an instance of BookManager
book_manager = BookManager()

# Iterate over the books attribute (which holds a list of Book objects)
for book in book_manager.books:
    print(book)

