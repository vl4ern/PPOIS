class Notification:
    def __init__(self, to, subject: str, body: str):
        self.to = to
        self.subject = subject
        self.body = body
        self.sent = False

    def send(self):
        self.sent = True