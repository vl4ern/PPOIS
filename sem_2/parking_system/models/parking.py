from typing import Dict, List
from datetime import datetime
import json
import os
from .car import Car
from .parking_spot import ParkingSpot
from .tariff import Tariff
from .service import Service

class Parking:
    """это будет main модель"""

    def __init__(self, name: str = "Модель автостоянки"):
        self.name = name
        self.spots: Dict[str, ParkingSpot] = {}
        self.cars: Dict[str, Car] = {}
        self.tariffs: Dict[str, Tariff] = {}
        self.services: Dict[str, Service] = {}
        self.total_income: float = 0.0
        self.security_status: str = "active"

    def add_spot(self, spot_id: str)->None:
        self.spots[spot_id] = ParkingSpot(spot_id) #add spot

    def add_tariff(self, tariff: Tariff)->None:
        self.tariffs[tariff.tariff_id] = tariff

    def add_service(self, service: Service)->None:
        self.services[service.service_id] = service

    def get_add_spots(self)->List[str]:
        return[spot_id for spot_id, spot in self.spots.items() if not spot.is_occupied]
    
    def get_occupied_spots(self)->List[str]:
        return[spot_id for spot_id, spot in self.spots.items() if spot.is_occupied]
    
    def to_dict(self)->dict:
        return{
            'name': self.name,
            'spots': {k: v.to_dict() for k, v in self.spots.items()},
            'cars': {k: v.to_dict() for k, v in self.cars.items()},
            'tariffs': {k: v.to_dict() for k, v in self.tariffs.items()},
            'services': {k: v.to_dict() for k, v in self.services.items()},
            'total_income': self.total_income,
            'security_status': self.security_status 
        }
    
    @staticmethod
    def from_dict(data: dict)->'Parking':
        parking = Parking(data['name'])
        parking.spots = {k: ParkingSpot.from_dict(v) for k, v in data['spots'].items()}
        parking.cars = {k: Car.from_dict(v) for k, v in data['cars'].items()}
        parking.tariffs = {k: Tariff.from_dict(v) for k, v in data['tariffs'].items()}
        parking.services = {k: Service.from_dict(v) for k, v in data['services'].items()}
        parking.total_income = data['total_income']
        parking.security_status = data['security_status']
        return parking
    
    def save_to_file(self, filename: str = "data/parking_data.json")->None:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.damp(self.to_dict(), f, ensure_ascii=False, indent=2)

    @staticmethod
    def load_from_file(filename: str = "data/parking_data.json")->'Parking':
        if not os.path.exists(filename):
            return Parking.create_default()
        
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return Parking.from_dict(data)
    
    @staticmethod
    def create_default()-> 'Parking':
        parking = Parking("Модель автостоянки")

        for i in range(1,15):
            spot_id = f"A{i:02d}"
            parking.add_spot(spot_id)

        parking.add_tariff(Tariff("standart", "Стандартный (1 час)", "2.0", "1","1"))
        parking.add_tariff(Tariff("four_hour", "Увеличенный (4 часа)", "7.0", "4","4"))
        parking.add_tariff(Tariff("day", "Суточный", "40.0", "24","24"))
        parking.add_tariff(Tariff("three_days", "Трех дневный", "125.0", "72","72"))

        parking.add_service(Service("wash", "Мойка авто", "230.0", "Полная мойка автомобиля."))
        parking.add_service(Service("charge", "Зарядка авто", "140.0", "Зарядка электрокара."))
        parking.add_service(Service("wifi", "Wi-fi на парковке", "15.0", "Высокоскоростной интернет по всей территории автостоянки."))
        parking.add_service(Service("security", "Повышенная охрана", "350.0", "Дополнительный контроль за автотранспортом в случае чп ремонт за счет компании."))

        return parking