from classes.Vehicle_classes.Vehicle import Vehicle
from classes.Exceptions.InvalidVehicleDataException import InvalidVehicleDataException

class Track(Vehicle):
    def __init__(self, vin, brand, model, year, max_load):
        super().__init__(vin, brand, model, year)
        self.max_load = max_load
        self.current_load = 0
        
    def load_cargo(self, weight):
        if weight > self.max_load:
            raise InvalidVehicleDataException("Грузоподъемность превышена")
        self.current_load = weight
        
    def get_vehicle_info(self):
        return f"{super().get_vehicle_info()} - Грузоподъемность: {self.max_load}кг"