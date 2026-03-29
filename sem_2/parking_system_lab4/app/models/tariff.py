from __future__ import annotations


class Tariff:
    def __init__(self, tariff_id: str, name: str, price: float, min_time: int = 1, max_time: int = 24) -> None:
        self.tariff_id = tariff_id
        self.name = name
        self.price = price
        self.min_time = min_time
        self.max_time = max_time

    def calculate_cost(self, duration: int) -> float:
        if duration < self.min_time or duration > self.max_time:
            raise ValueError(
                f"Для тарифа '{self.name}' допустимое время: от {self.min_time} до {self.max_time} ч."
            )
        return round(self.price, 2)

    def to_dict(self) -> dict:
        return {
            "tariff_id": self.tariff_id,
            "name": self.name,
            "price": self.price,
            "min_time": self.min_time,
            "max_time": self.max_time,
        }

    @staticmethod
    def from_dict(data: dict) -> "Tariff":
        return Tariff(
            tariff_id=data["tariff_id"],
            name=data["name"],
            price=float(data["price"]),
            min_time=int(data["min_time"]),
            max_time=int(data["max_time"]),
        )
