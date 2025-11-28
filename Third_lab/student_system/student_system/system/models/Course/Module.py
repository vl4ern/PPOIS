class Module:
    def __init__(self, name: str, lessons: int = 10):
        self.name = name
        self.lessons = lessons

    def workload(self):
        return self.lessons * 2