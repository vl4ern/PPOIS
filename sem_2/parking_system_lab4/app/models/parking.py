from __future__ import annotations

import json
from pathlib import Path

from app.models.car import Car
from app.models.parking_spot import ParkingSpot
from app.models.service import Service
from app.models.tariff import Tariff


class Parking:
    def __init__(self, name: str = "Модель автостоянки") -> None:
        self.name = name
        self.spots: dict[str, ParkingSpot] = {}
        self.cars: dict[str, Car] = {}
        self.tariffs: dict[str, Tariff] = {}
        self.services: dict[str, Service] = {}
        self.total_income: float = 0.0
        self.security_status: str = "active"

    def add_spot(self, spot_id: str) -> None:
        self.spots[spot_id] = ParkingSpot(spot_id)

    def add_tariff(self, tariff: Tariff) -> None:
        self.tariffs[tariff.tariff_id] = tariff

    def add_service(self, service: Service) -> None:
        self.services[service.service_id] = service

    def get_free_spots(self) -> list[str]:
        return [spot_id for spot_id, spot in self.spots.items() if not spot.is_occupied]

    def get_occupied_spots(self) -> list[str]:
        return [spot_id for spot_id, spot in self.spots.items() if spot.is_occupied]

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "spots": {k: v.to_dict() for k, v in self.spots.items()},
            "cars": {k: v.to_dict() for k, v in self.cars.items()},
            "tariffs": {k: v.to_dict() for k, v in self.tariffs.items()},
            "services": {k: v.to_dict() for k, v in self.services.items()},
            "total_income": self.total_income,
            "security_status": self.security_status,
        }

    @staticmethod
    def from_dict(data: dict) -> "Parking":
        parking = Parking(data["name"])
        parking.spots = {k: ParkingSpot.from_dict(v) for k, v in data["spots"].items()}

        # Нормализуем номера автомобилей при загрузке.
        # Это исправляет старые сохранения, где номер мог попасть в JSON
        # в смешанном регистре и потом не находился через поиск/выдачу,
        # потому что во всех сценариях ввода мы ищем по UPPERCASE.
        parking.cars = {}
        for raw_plate, car_data in data["cars"].items():
            car = Car.from_dict(car_data)
            normalized_plate = car.license_plate.strip().upper()
            car.license_plate = normalized_plate
            parking.cars[normalized_plate] = car

        for spot_id, spot in parking.spots.items():
            if spot.car_plate:
                spot.car_plate = spot.car_plate.strip().upper()

                # Если в старом файле место занято, но ключ в cars был записан
                # в другом регистре, восстанавливаем корректную связку.
                if spot.car_plate in parking.cars:
                    parking.cars[spot.car_plate].spot_id = spot_id

        parking.tariffs = {k: Tariff.from_dict(v) for k, v in data["tariffs"].items()}
        parking.services = {k: Service.from_dict(v) for k, v in data["services"].items()}
        parking.total_income = float(data.get("total_income", 0.0))
        parking.security_status = data.get("security_status", "active")
        return parking

    def save_to_file(self, filename: Path) -> None:
        filename.parent.mkdir(parents=True, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(self.to_dict(), file, ensure_ascii=False, indent=2)

    @staticmethod
    def load_from_file(filename: Path) -> "Parking":
        if not filename.exists():
            parking = Parking.create_default()
            parking.save_to_file(filename)
            return parking

        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        return Parking.from_dict(data)

    @staticmethod
    def create_default() -> "Parking":
        parking = Parking("Автостоянка 78")

        for index in range(1, 15):
            parking.add_spot(f"A{index:02d}")

        parking.add_tariff(Tariff("standard", "Стандартный (1 час)", 2.0, 1, 1))
        parking.add_tariff(Tariff("four_hours", "Увеличенный (4 часа)", 7.0, 4, 4))
        parking.add_tariff(Tariff("day", "Суточный", 40.0, 24, 24))
        parking.add_tariff(Tariff("three_days", "Трёхдневный", 125.0, 72, 72))

        parking.add_service(Service("wash", "Мойка авто", 230.0, "Полная мойка автомобиля."))
        parking.add_service(Service("charge", "Зарядка авто", 140.0, "Зарядка электромобиля."))
        parking.add_service(Service("wifi", "Wi‑Fi на парковке", 15.0, "Доступ к интернету на территории автостоянки."))
        parking.add_service(Service("security", "Повышенная охрана", 350.0, "Дополнительный контроль за транспортом."))

        return parking
