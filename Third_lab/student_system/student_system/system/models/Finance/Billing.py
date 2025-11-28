class Billing:
    def __init__(self):
        self.invoices = []

    def create_invoice(self, owner, amount: float):
        self.invoices.append((owner, amount))
        return len(self.invoices) - 1