from system.models.Student.EnrollmentRecord import EnrollmentRecord
from system.models.Student.Student import Student
from ..models.Teacher import Teacher, Office
from ..models.Course import Course, CourseSchedule, Module, Syllabus
from ..models.Schedule import TimeSlot
from ..exceptions import DuplicateIDError, InvalidSelectionError

class Registrar:
    def __init__(self):
        self.students = {}
        self.teachers = {}

    def register_student(self, first_name, last_name, student_id, email=""):
        if student_id in self.students:
            raise DuplicateIDError("Student id exists")
        s = Student(first_name, last_name, student_id, email=email)
        self.students[student_id] = s
        return s

    def add_teacher(self, teacher: Teacher):
        self.teachers[teacher.teacher_id] = teacher

    def available_teachers(self):
        return list(self.teachers.values())

    def enroll_student(self, student_id: str, teacher_id: str, course_code: str, timeslot_index: int):
        if student_id not in self.students:
            raise InvalidSelectionError("no student")
        if teacher_id not in self.teachers:
            raise InvalidSelectionError("no teacher")
        student = self.students[student_id]
        teacher = self.teachers[teacher_id]
        # find course
        course = None
        for c in teacher.courses:
            if c.code == course_code:
                course = c
        if not course:
            raise InvalidSelectionError("no course")
        if timeslot_index < 0 or timeslot_index >= len(course.schedule_options):
            raise InvalidSelectionError("timeslot")
        timeslot = course.schedule_options[timeslot_index]
        # create enrollment
        record = EnrollmentRecord(student, course)
        student.enroll(course)
        return {"student": student, "teacher": teacher, "course": course, "timeslot": timeslot}