class Scholarship:
    def __init__(self, awardee, amount: float, reason: str = ""):
        self.awardee = awardee
        self.amount = amount
        self.reason = reason

    def award(self):
        if hasattr(self.awardee, "account"):
            self.awardee.account.deposit(self.amount)
            return True
        return False