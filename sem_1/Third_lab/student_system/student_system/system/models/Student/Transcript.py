class Transcript:
    def __init__(self):
        self.entries = [] 

    def add_grade(self, grade_record):
        self.entries.append(grade_record)

    def gpa(self):
        if not self.entries:
            return 0.0
        total = sum([e.grade for e in self.entries])
        return total / len(self.entries)