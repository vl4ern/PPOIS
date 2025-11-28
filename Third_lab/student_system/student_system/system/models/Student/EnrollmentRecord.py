from ..Student.Student import Student
class EnrollmentRecord:
    def __init__(self, student: Student, course, status: str = "active"):
        self.student = student
        self.course = course
        self.status = status

    def is_active(self):
        return self.status == "active"