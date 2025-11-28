class Office:
    def __init__(self, building: str, room: str, phone: str = ""):
        self.building = building
        self.room = room
        self.phone = phone

    def location(self):
        return f"{self.building} {self.room}"