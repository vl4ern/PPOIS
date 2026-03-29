from __future__ import annotations

from app.models.car import Car
from app.models.parking import Parking
from app.services.parking_service import ParkingService
from app.storage import DATA_FILE


class ParkingFacade:
    def __init__(self) -> None:
        self.parking = Parking.load_from_file(DATA_FILE)
        self.service = ParkingService(self.parking)

    def save(self) -> None:
        self.parking.save_to_file(DATA_FILE)

    def stats(self) -> dict:
        traffic = self.service.optimize_traffic()
        return {
            "name": self.parking.name,
            "total_spots": traffic["total_spots"],
            "free_spots": traffic["free_spots"],
            "occupied_spots": traffic["occupied_spots"],
            "occupancy_rate": traffic["occupancy_rate"],
            "free_spots_list": traffic["free_spots_list"],
            "recommendation": traffic["recommendation"],
            "income": round(self.parking.total_income, 2),
        }

    def cars_for_view(self) -> list[dict]:
        rows: list[dict] = []
        for car in self.parking.cars.values():
            rows.append(
                {
                    "license_plate": car.license_plate,
                    "model": car.model,
                    "year": car.year,
                    "owner": car.owner,
                    "spot_id": car.spot_id,
                    "paid": car.paid,
                    "entry_time": car.entry_time.strftime("%d.%m.%Y %H:%M") if car.entry_time else "—",
                    "services": [self.parking.services[service_id].name for service_id in car.services],
                }
            )
        return rows

    def tariffs_for_view(self) -> list[dict]:
        return [
            {
                "id": tariff.tariff_id,
                "name": tariff.name,
                "price": tariff.price,
                "min_time": tariff.min_time,
                "max_time": tariff.max_time,
            }
            for tariff in self.parking.tariffs.values()
        ]

    def services_for_view(self) -> list[dict]:
        return [
            {
                "id": service.service_id,
                "name": service.name,
                "price": service.price,
                "description": service.description,
            }
            for service in self.parking.services.values()
        ]

    def place_car(self, license_plate: str, model: str, year: int, owner: str, spot_id: str) -> None:
        car = Car(license_plate=license_plate.strip().upper(), model=model.strip(), year=year, owner=owner.strip())
        self.service.place_car(car, spot_id)
        self.save()

    def pay_for_parking(self, license_plate: str, tariff_id: str) -> dict:
        result = self.service.pay_for_parking(license_plate.strip().upper(), tariff_id)
        self.save()
        return result

    def add_service(self, license_plate: str, service_id: str) -> float:
        price = self.service.add_service_to_car(license_plate.strip().upper(), service_id)
        self.save()
        return price

    def remove_car(self, license_plate: str) -> dict:
        result = self.service.remove_car(license_plate.strip().upper())
        self.save()
        return result

    def reset_income(self) -> None:
        self.service.reset_income()
        self.save()

    def security_info(self, license_plate: str) -> dict:
        return self.service.check_security(license_plate.strip().upper())
