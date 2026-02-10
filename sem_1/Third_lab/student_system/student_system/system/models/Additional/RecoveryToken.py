class RecoveryToken:
    def __init__(self, user, token: str):
        self.user = user
        self.token = token
        self.used = False

    def use(self):
        if self.used:
            return False
        self.used = True
        return True