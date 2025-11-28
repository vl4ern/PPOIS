class Author:
    def __init__(self, name: str, born: str = ""):
        self.name = name
        self.born = born

    def profile(self):
        return {"name": self.name, "born": self.born}