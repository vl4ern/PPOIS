class Course:
    def __init__(self, code: str, title: str, credits: int = 3):
        self.code = code
        self.title = title
        self.credits = credits
        self.modules = []
        self.syllabus = None
        self.schedule_options = [] 

    def add_module(self, module):
        self.modules.append(module)

    def available_times(self):
        return [t.describe() for t in self.schedule_options]