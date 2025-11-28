class Dorm:
    def __init__(self, name: str, capacity: int = 100):
        self.name = name
        self.capacity = capacity
        self.rooms = []

    def vacancy(self):
        return self.capacity - sum(1 for r in self.rooms if r.occupied)