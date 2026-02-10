from datetime import datetime
from classes.Exceptions.PaymentFailedException import PaymentFailedException

class Invoice:
    def __init__(self, invoice_id, work_order):
        self.invoice_id = invoice_id
        self.work_order = work_order
        self.issue_date = datetime.now()
        self.is_paid = False
        self.payment_method = None
    
    def process_payment(self, payment_method, amount):
        if amount < self.work_order.total_cost:
            raise PaymentFailedException("Недостаточная сумма платежа")
        self.payment_method = payment_method
        self.is_paid = True
    
    def __str__(self):
        return f"Чек #{self.invoice_id} - ${self.work_order.total_cost:.2f}"