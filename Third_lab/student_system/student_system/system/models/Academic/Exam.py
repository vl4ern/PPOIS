class Exam:
    def __init__(self, course, date: str):
        self.course = course
        self.date = date

    def schedule(self):
        return f"Exam for {self.course.code} on {self.date}"