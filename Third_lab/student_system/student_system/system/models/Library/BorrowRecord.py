from .Book import Book
class BorrowRecord:
    def __init__(self, book: Book, borrower, due_date: str):
        self.book = book
        self.borrower = borrower
        self.due_date = due_date

    def is_overdue(self, today_str: str):
        return False