class SearchStrategy :
    def search(self,books):
        pass
3
class AuthorSearchStrategy(SearchStrategy):
    def __init__(self, author):
        self.author=author

    def search(self,books):
        return [book for book in books if self.author in book.author]

class NameSearchStrategy(SearchStrategy):
    def __init__(self, name):
        self.name = name

    def search(self, books):
        return [book for book in books if self.name in book.name]

class GenreSearchStrategy(SearchStrategy):
    def __init__(self, genre):
        self.genre = genre

    def search(self, books):
        return [book for book in books if self.genre in book.genre]


