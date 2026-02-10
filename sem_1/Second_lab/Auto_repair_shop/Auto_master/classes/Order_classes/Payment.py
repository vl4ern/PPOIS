from datetime import datetime

class Payment:
    def __init__(self, payment_id, amount, payment_method):
        self.payment_id = payment_id
        self.amount = amount
        self.payment_method = payment_method
        self.payment_date = datetime.now()
        self.status = "Полный"
    
    def __str__(self):
        return f"Оплата #{self.payment_id} - ${self.amount:.2f}"