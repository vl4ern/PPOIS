class Event:
    def __init__(self, title: str, date: str, location: str = ""):
        self.title = title
        self.date = date
        self.location = location

    def describe(self):
        return f"{self.title} at {self.location} on {self.date}"