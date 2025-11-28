class Scheduler:
    def __init__(self):
        self.entries = []  

    def add_entry(self, entry):
        self.entries.append(entry)

    def find_entries_for(self, person):
        return [e for e in self.entries if getattr(e, "owner", None) == person]