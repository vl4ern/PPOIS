from dataclasses import dataclass
@dataclass
class ContactInfo:
    def __init__(self, email: str, phone: str, alt_phone: str = ""):
        self.email = email
        self.phone = phone
        self.alt_phone = alt_phone

    def reachable(self):
        return bool(self.email or self.phone)