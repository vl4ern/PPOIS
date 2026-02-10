from .Room import Room
class Lease:
    def __init__(self, resident, room: Room, start_date: str, end_date: str):
        self.resident = resident
        self.room = room
        self.start_date = start_date
        self.end_date = end_date

    def is_active(self, date_str: str):
        return True