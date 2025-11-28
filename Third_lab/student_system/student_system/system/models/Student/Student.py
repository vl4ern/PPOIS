from system.models.Person.Person import Person
class Student(Person):
    def __init__(self, first_name: str, last_name: str, student_id: str, email: str = ""):
        super().__init__(first_name, last_name, email=email)
        self.student_id = student_id
        self.enrolled_courses = []
        self.transcript = None
        self.housing = None

    def enroll(self, course):
        """Добавляет курс студенту."""
        self.enrolled_courses.append(course)
