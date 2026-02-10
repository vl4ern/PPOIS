class Library:
    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address
        self.catalog = []  
        self.borrow_records = []

    def add_book(self, book):
        self.catalog.append(book)

    def find_book(self, title: str):
        return [b for b in self.catalog if title.lower() in b.title.lower()]