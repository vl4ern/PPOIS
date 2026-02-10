from ..models.Finance import Card, Transaction
from ..models.Library import Library, Book, BorrowRecord
from ..models.Schedule import TimeSlot, CalendarEntry, Scheduler

class PaymentProcessor:
    def __init__(self):
        self.log = []

    def verify_card(self, card: Card, cvv: str) -> bool:
        return bool(card.card_number and not card.blocked)

    def transfer(self, from_card: Card, to_card: Card, amount: float) -> bool:
        t = Transaction(from_card, to_card, amount, reference="service-transfer")
        return t.execute()

class BehaviorManager:
    def __init__(self):
        self.behaviors = []

    def register(self, name: str, fn):
        self.behaviors.append((name, fn))

    def run_all(self):
        for name, fn in self.behaviors:
            try:
                fn()
            except Exception:
                pass

class NotificationService:
    def __init__(self):
        self.sent = []

    def notify(self, notification):
        notification.send()
        self.sent.append(notification)

class LibraryAssistant:
    def __init__(self, library: Library):
        self.library = library

    def checkout_book(self, book: Book, borrower):
        if book.checkout(borrower):
            br = BorrowRecord(book, borrower, due_date="2025-12-31")
            self.library.borrow_records.append(br)
            return br
        return None