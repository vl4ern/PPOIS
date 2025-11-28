class Account:
    def __init__(self, owner, balance: float = 0.0):
        self.owner = owner
        self.balance = balance
        self.transactions = []

    def deposit(self, amount: float):
        self.balance += amount
        self.transactions.append(("deposit", amount))
        return self.balance

    def withdraw(self, amount: float):
        if amount > self.balance:
            raise Exception("insufficient")
        self.balance -= amount
        self.transactions.append(("withdraw", amount))
        return self.balance