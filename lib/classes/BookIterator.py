class BookIterator:
    def __init__(self, books):
        if books is None:
            books = []  # Ensure books is always a list, even if None is passed
        self.books = books
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.books):
            book = self.books[self.index]
            self.index += 1
            return book
        else:
            raise StopIteration  # Raise StopIteration when no more books are left

    def __len__(self):
        # Allow len() to work by returning the number of books
        return len(self.books)

    def __getitem__(self, index):
        # Allow subscripting by accessing the books list
        return self.books[index]
