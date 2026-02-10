class University:
    def __init__(self, name: str):
        self.name = name
        self.departments = []
        self.campuses = []

    def add_department(self, dept):
        self.departments.append(dept)

    def find_course(self, code: str):
        for d in self.departments:
            for c in d.courses:
                if c.code == code:
                    return c
        return None