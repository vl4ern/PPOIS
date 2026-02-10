class Degree:
    def __init__(self, name: str, level: str):
        self.name = name
        self.level = level
        self.requirements = []

    def add_requirement(self, req):
        self.requirements.append(req)