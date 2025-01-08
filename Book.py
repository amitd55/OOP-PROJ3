from FileManagement import FileManagement

class Book:
    def __init__(self,name,author,year,copies,genre,is_loaned):
        self._name=name
        self._author=author
        self._year=year
        self._copies=copies
        self._genre=genre
        self._is_loaned = is_loaned
        self._borrowed_copies=[False]*copies
        self._count_total_borrowed=0
        
    def __str__(self):
        return f"Book(name='{self._name}', author='{self._author}', year={self._year}, copies={self._copies}, genre='{self._genre}', is_loaned={self._is_loaned}, is_popular={self._is_popular})"

    @property
    def name(self):
        return self._name

    @property
    def author(self):
        return self._author

    @property
    def year(self):
        return self._year

    @property
    def copies(self):
        return self._copies

    @property
    def genre(self):
        return self._genre

    @property
    def is_loaned(self):
        return self._is_loaned
    
    @property
    def borrowed_copies(self):
        return self._borrowed_copies.count(True)
    
    def update_copies(self,value):
        if value >0 :
            self._copies+=value
            self._borrowed_copies.extend([False]*value)


    def available_copies(self):
        return  self._borrowed_copies.count(False)


    def borrow_book(self):
        if self.available_copies() > 0 :
            for i in range (len(self._borrowed_copies)):
                if not self._borrowed_copies[i]:
                    self._borrowed_copies[i]=True
                    self._count_total_borrowed+=1
                    break


    def return_book(self):
        if self._borrowed_copies > 0:
            for i in range(len(self._borrowed_copies)):
                if self._borrowed_copies[i]:
                    self._borrowed_copies[i] = False
                    break
    
    def extend_num_of_copies(self,num):
        self.copies(num)




