from ..Schedule.TimeSlot import TimeSlot
class CalendarEntry:
    def __init__(self, owner, timeslot: TimeSlot, location: str = ""):
        self.owner = owner
        self.timeslot = timeslot
        self.location = location

    def conflicts_with(self, other):
        return self.timeslot.day == other.timeslot.day and self.timeslot.start == other.timeslot.start
    def enroll(self, course):
        if course not in self.enrolled_courses:
            self.enrolled_courses.append(course)
            return True
        return False

    def drop(self, course):
        if course in self.enrolled_courses:
            self.enrolled_courses.remove(course)
            return True
        return False