from __future__ import annotations

from datetime import datetime
from typing import Optional


class Car:
    def __init__(self, license_plate: str, model: str, year: int, owner: str) -> None:
        self.license_plate = license_plate
        self.model = model
        self.year = year
        self.owner = owner
        self.entry_time: Optional[datetime] = None
        self.spot_id: Optional[str] = None
        self.paid: bool = False
        self.paid_time: int = 0
        self.services: list[str] = []

    def to_dict(self) -> dict:
        return {
            "license_plate": self.license_plate,
            "model": self.model,
            "year": self.year,
            "owner": self.owner,
            "entry_time": self.entry_time.isoformat() if self.entry_time else None,
            "spot_id": self.spot_id,
            "paid": self.paid,
            "paid_time": self.paid_time,
            "services": self.services,
        }

    @staticmethod
    def from_dict(data: dict) -> "Car":
        car = Car(
            license_plate=data["license_plate"],
            model=data["model"],
            year=int(data["year"]),
            owner=data["owner"],
        )
        if data.get("entry_time"):
            car.entry_time = datetime.fromisoformat(data["entry_time"])
        car.spot_id = data.get("spot_id")
        car.paid = bool(data.get("paid", False))
        car.paid_time = int(data.get("paid_time", 0))
        car.services = list(data.get("services", []))
        return car
