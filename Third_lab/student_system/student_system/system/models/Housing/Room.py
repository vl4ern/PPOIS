class Room:
    def __init__(self, number: str, floor: int, occupied: bool = False):
        self.number = number
        self.floor = floor
        self.occupied = occupied

    def assign(self, resident):
        if self.occupied:
            return False
        self.occupied = True
        self.resident = resident
        return True