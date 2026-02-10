from .TimeSlot import TimeSlot
class CalendarEntry:
    def __init__(self, owner, timeslot: TimeSlot, location: str = ""):
        self.owner = owner
        self.timeslot = timeslot
        self.location = location

    def conflicts_with(self, other):
        return self.timeslot.day == other.timeslot.day and self.timeslot.start == other.timeslot.start