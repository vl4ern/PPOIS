from dataclasses import dataclass
@dataclass
class Address:
    def __init__(self, street: str, city: str, zip_code: str, country: str):
        self.street = street
        self.city = city
        self.zip_code = zip_code
        self.country = country

    def formatted(self):
        return f"{self.street}, {self.city}, {self.zip_code}, {self.country}"