from classes.Exceptions.InvalidVehicleDataException import InvalidVehicleDataException
from datetime import datetime

class Vehicle:
    def __init__(self, vin, brand, model, year):
        if not vin or len(vin) != 17:
            raise InvalidVehicleDataException("VIN должен быть длиной 17 символов.")
        self.vin = vin
        self.brand = brand
        self.model = model
        self.year = year
        self.mileage = 0
        self.last_service_date = None
        
    def update_mileage(self, new_mileage):
        if new_mileage < self.mileage:
            raise InvalidVehicleDataException("Пробег не может быть уменьшен")
        self.mileage = new_mileage
        
    def get_vehicle_info(self):
        return f"{self.brand}{self.model} ({self.year})"
    
    def __str__(self):
        return self.get_vehicle_info()