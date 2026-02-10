class Qualification:
    def __init__(self, title: str, institution: str, year: int):
        self.title = title
        self.institution = institution
        self.year = year

    def short(self):
        return f"{self.title} ({self.year})"