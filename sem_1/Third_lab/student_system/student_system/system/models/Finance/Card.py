from Account import Account
class Card:
    def __init__(self, account: Account, card_number: str, holder_name: str):
        self.account = account
        self.card_number = card_number
        self.holder_name = holder_name
        self.blocked = False

    def block(self):
        self.blocked = True

    def unblock(self):
        self.blocked = False