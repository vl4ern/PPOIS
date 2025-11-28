from ..Course import Course
class CourseSchedule:
    def __init__(self, course: Course, timeslot):
        self.course = course
        self.timeslot = timeslot

    def is_conflict(self, other):
        return self.timeslot == other.timeslot