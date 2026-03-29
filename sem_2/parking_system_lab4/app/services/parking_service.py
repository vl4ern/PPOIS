from __future__ import annotations

from datetime import datetime

from app.models.car import Car
from app.models.parking import Parking


class SpotOccupiedError(Exception):
    pass


class CarNotFoundError(Exception):
    pass


class PaymentError(Exception):
    pass


class ParkingService:
    def __init__(self, parking: Parking) -> None:
        self.parking = parking

    def place_car(self, car: Car, spot_id: str) -> bool:
        if spot_id not in self.parking.spots:
            raise ValueError(f"Парковочное место {spot_id} не существует.")

        spot = self.parking.spots[spot_id]
        if spot.is_occupied:
            raise SpotOccupiedError(f"Место {spot_id} уже занято.")

        spot.is_occupied = True
        spot.car_plate = car.license_plate
        car.spot_id = spot_id
        car.entry_time = datetime.now()
        self.parking.cars[car.license_plate] = car
        return True

    def pay_for_parking(self, license_plate: str, tariff_id: str) -> dict:
        if license_plate not in self.parking.cars:
            raise CarNotFoundError(f"Автомобиль {license_plate} не найден на парковке.")
        if tariff_id not in self.parking.tariffs:
            raise ValueError(f"Тариф {tariff_id} не существует.")

        car = self.parking.cars[license_plate]
        tariff = self.parking.tariffs[tariff_id]
        cost = tariff.calculate_cost(tariff.min_time)

        car.paid = True
        car.paid_time = tariff.min_time
        self.parking.total_income += cost

        return {
            "cost": cost,
            "duration": tariff.min_time,
            "tariff_name": tariff.name,
        }

    def add_service_to_car(self, license_plate: str, service_id: str) -> float:
        if license_plate not in self.parking.cars:
            raise CarNotFoundError(f"Автомобиль {license_plate} не найден.")
        if service_id not in self.parking.services:
            raise ValueError(f"Услуга {service_id} не существует.")

        car = self.parking.cars[license_plate]
        service = self.parking.services[service_id]

        if service_id not in car.services:
            car.services.append(service_id)
            self.parking.total_income += service.price
        return service.price

    def remove_car(self, license_plate: str) -> dict:
        if license_plate not in self.parking.cars:
            raise CarNotFoundError(f"Автомобиль {license_plate} не найден.")

        car = self.parking.cars[license_plate]
        if not car.paid:
            raise PaymentError("Парковка не оплачена.")

        spot = self.parking.spots[car.spot_id]
        spot.is_occupied = False
        spot.car_plate = None
        del self.parking.cars[license_plate]

        return {
            "spot_id": car.spot_id,
            "duration": car.paid_time,
            "license_plate": license_plate,
        }

    def check_security(self, license_plate: str) -> dict:
        if license_plate not in self.parking.cars:
            raise CarNotFoundError(f"Автомобиль {license_plate} не найден.")

        car = self.parking.cars[license_plate]
        return {
            "license_plate": license_plate,
            "owner": car.owner,
            "spot_id": car.spot_id,
            "entry_time": car.entry_time.strftime("%d.%m.%Y %H:%M:%S") if car.entry_time else "—",
            "security_status": self.parking.security_status,
            "services": [self.parking.services[service_id].name for service_id in car.services],
        }

    def optimize_traffic(self) -> dict:
        total_spots = len(self.parking.spots)
        free_spots = self.parking.get_free_spots()
        occupied_spots = self.parking.get_occupied_spots()
        occupancy_rate = round((len(occupied_spots) / total_spots) * 100, 1) if total_spots else 0.0

        return {
            "total_spots": total_spots,
            "free_spots": len(free_spots),
            "occupied_spots": len(occupied_spots),
            "occupancy_rate": occupancy_rate,
            "free_spots_list": free_spots,
            "recommendation": self._get_traffic_recommendation(occupancy_rate),
        }

    def reset_income(self) -> None:
        self.parking.total_income = 0.0

    @staticmethod
    def _get_traffic_recommendation(occupancy_rate: float) -> str:
        if occupancy_rate < 30:
            return "Нагрузка низкая. Можно направлять машины на любые свободные места."
        if occupancy_rate < 70:
            return "Нагрузка средняя. Система работает стабильно, движение без перегрузок."
        if occupancy_rate < 90:
            return "Нагрузка высокая. Стоит активнее контролировать распределение машин."
        return "Почти полная загрузка. Необходимо оперативно освобождать места и ускорять обслуживание."
