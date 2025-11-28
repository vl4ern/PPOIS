from .Card import Card
class Transaction:
    def __init__(self, from_card: Card, to_card: Card, amount: float, reference: str = ""):
        self.from_card = from_card
        self.to_card = to_card
        self.amount = amount
        self.reference = reference

    def execute(self):
        if self.from_card.blocked or self.to_card.blocked:
            return False
        if self.from_card.account.balance < self.amount:
            raise Exception("insufficient funds")
        self.from_card.account.withdraw(self.amount)
        self.to_card.account.deposit(self.amount)
        return True