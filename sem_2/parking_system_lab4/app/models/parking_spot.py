from __future__ import annotations

from typing import Optional


class ParkingSpot:
    def __init__(self, spot_id: str) -> None:
        self.spot_id = spot_id
        self.is_occupied: bool = False
        self.car_plate: Optional[str] = None
        self.tariff_id: str = "standard"

    def to_dict(self) -> dict:
        return {
            "spot_id": self.spot_id,
            "is_occupied": self.is_occupied,
            "car_plate": self.car_plate,
            "tariff_id": self.tariff_id,
        }

    @staticmethod
    def from_dict(data: dict) -> "ParkingSpot":
        spot = ParkingSpot(data["spot_id"])
        spot.is_occupied = bool(data.get("is_occupied", False))
        spot.car_plate = data.get("car_plate")
        spot.tariff_id = data.get("tariff_id", "standard")
        return spot
