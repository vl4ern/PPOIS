class GradeRecord:
    def __init__(self, course_code: str, grade: float, credits: int = 3):
        self.course_code = course_code
        self.grade = grade
        self.credits = credits