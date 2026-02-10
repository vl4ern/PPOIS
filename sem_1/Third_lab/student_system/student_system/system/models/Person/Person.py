from dataclasses import dataclass
@dataclass
class Person:
    first_name: str
    last_name: str
    email: str = ""
    phone: str = ""
    metadata: dict = None

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def contact_card(self) -> dict:
        return {"name": self.full_name(), "email": self.email, "phone": self.phone}