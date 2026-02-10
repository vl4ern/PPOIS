class Badge:
    def __init__(self, name: str, level: int = 1):
        self.name = name
        self.level = level

    def promote(self):
        self.level += 1