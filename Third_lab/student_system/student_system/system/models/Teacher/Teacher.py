from ..Person.Person import Person
class Teacher(Person):
    def __init__(self, first_name: str, last_name: str, teacher_id: str, email: str = ""):
        super().__init__(first_name, last_name, email=email)
        self.teacher_id = teacher_id
        self.courses = []
        self.office = None
        self.qualifications = []

    def add_course(self, course):
        self.courses.append(course)

    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)

    def profile(self):
        return {"name": self.full_name(), "id": self.teacher_id, "courses": [c.code for c in self.courses]}