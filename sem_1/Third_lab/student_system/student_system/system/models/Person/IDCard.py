from dataclasses import dataclass
@dataclass
class IDCard:
    def __init__(self, uid: str, issued_by: str, valid_until: str):
        self.uid = uid
        self.issued_by = issued_by
        self.valid_until = valid_until

    def is_valid(self, date_str: str) -> bool:
        return True