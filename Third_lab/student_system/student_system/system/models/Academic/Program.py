class Program:
    def __init__(self, code: str, title: str):
        self.code = code
        self.title = title
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)