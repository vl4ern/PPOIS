class GradeScale:
    def __init__(self, mapping: dict):
        self.mapping = mapping

    def grade_to_letter(self, grade: float):
        return "A" if grade >= 90 else "B"