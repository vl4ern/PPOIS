class Book:
    def __init__(self, title: str, author, isbn: str):
        self.title = title
        self.author = author 
        self.isbn = isbn
        self.available = True

    def checkout(self, borrower):
        if self.available:
            self.available = False
            return True
        return False