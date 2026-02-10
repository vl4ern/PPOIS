class TimeSlot:
    def __init__(self, day: str, start: str, end: str, label: str = ""):
        self.day = day
        self.start = start
        self.end = end
        self.label = label

    def describe(self):
        return f"{self.day} {self.start}-{self.end} {self.label}"