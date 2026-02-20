from typing import List, Optional
from models.car import Car
from models.parking import Parking
from datetime import datetime

class SpotOccuoiedError(Exception):
    pass

class CArNotFound(Exception):
    pass

class PaymentError(Exception):
    pass

class PaskingService:
    def __init__(self, parking: Parking):
        self.parking = parking

    def place_car(self, car: Car, spot_id: str)-> bool:
        if spot_id not in self.parking.spots:
            raise ValueError(f"Парковочное место {spot_id} не существует!")
        
        spot = self.parking.spots[spot_id]

        if spot.is_occupied:
            raise SpotOccuoiedError(f"Место {spot_id} уже занято!")
        
        spot.is_occupied = True
        spot.car_plate = car.license
        car.spot_id = spot_id
        car.entry_time = datetime.now()

        self.parking.cars[car.license] = car

        return True
    
    def pay_for_parking(self, license: str, tariff_id: str)->dict:
        if license not in self.parking.cars:
            raise CArNotFound(f"Автомобиль {license} не найден на парковке!")
        
        if tariff_id not in self.parking.tariffs:
            raise ValueError(f"Тариф {tariff_id} не существует!")
        
        car = self.parking.cars[license]
        tariff = self.parking.tariffs[tariff_id]

        cost = tariff.calculate_cost(int(tariff.min_time))

        car.paid = True
        car.paid_time = int(tariff.min_time)

        self.parking.total_income += cost

        return{
            'cost': cost,
            'time': tariff.min_time,
            'tariff_name': tariff.name
        }
    
    def add_service_to_car(self, license: str, service_id: str) -> float:
        if license not in self.parking.cars:
            raise CArNotFound(f"Автомобиль {license} не найден")
        
        if service_id not in self.parking.services:
            raise ValueError(f"Услуга {service_id} не существует")
        
        car = self.parking.cars[license]
        service = self.parking.services[service_id]
        
        # Добавляем услугу
        if service_id not in car.services:
            car.services.append(service_id)
        
        # Добавляем к доходу
        self.parking.total_income += service.price
        
        return service.price
    
    def remove_car(self, license: str)->dict:
        if license not in self.parking.cars:
            raise CArNotFound(f"Автомобиль {license} не найден")
        
        car = self.parking.cars[license]
        
        if not car.paid:
            raise PaymentError("Парковка не оплачена")
        
        # Освобождаем место
        spot = self.parking.spots[car.spot_id]
        spot.is_occupied = False
        spot.car_plate = None
        
        # Удаляем автомобиль
        del self.parking.cars[license]

        return {
            'spot_id': car.spot_id,
            'duration': car.paid_time,
            'license_plate': license
        }
    
    def check_security(self, license: str) -> dict:
        if license not in self.parking.cars:
            raise CArNotFound(f"Автомобиль {license} не найден")
        
        car = self.parking.cars[license]
        
        return {
            'license_plate': license,
            'owner': car.owner,
            'spot_id': car.spot_id,
            'entry_time': car.entry_time.isoformat() if car.entry_time else None,
            'security_status': self.parking.security_status,
            'services': [self.parking.services[sid].name for sid in car.services]
            }
    
    def optimize_traffic(self) -> dict:
        free_spots = self.parking.get_free_spots()
        occupied_spots = self.parking.get_occupied_spots()
        
        occupancy_rate = len(occupied_spots) / len(self.parking.spots) * 100
        
        return {
            'total_spots': len(self.parking.spots),
            'free_spots': len(free_spots),
            'occupied_spots': len(occupied_spots),
            'occupancy_rate': round(occupancy_rate, 1),
            'free_spots_list': free_spots,
            'recommendation': self._get_traffic_recommendation(occupancy_rate)
        }
    
    def _get_traffic_recommendation(self, occupancy_rate: float) -> str:
        if occupancy_rate < 30:
            return 
        elif occupancy_rate < 70:
            return 
        elif occupancy_rate < 90:
            return 
        else:
            return 