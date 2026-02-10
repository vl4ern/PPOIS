class Department:
    def __init__(self, name: str, head=None):
        self.name = name
        self.head = head
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)