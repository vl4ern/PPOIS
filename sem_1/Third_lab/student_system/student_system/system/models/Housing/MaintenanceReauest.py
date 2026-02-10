from .Room import Room
class MaintenanceRequest:
    def __init__(self, room: Room, issue: str):
        self.room = room
        self.issue = issue
        self.status = "open"

    def resolve(self):
        self.status = "closed"