from classes.Vehicle_classes.Vehicle import Vehicle

class Motorcycle(Vehicle):
    def __init__(self, vin, brand, model, year, engine_size):
        super().__init__(vin, brand, model, year)
        self.engine_size = engine_size
        self.motorcycle_type = "Стандарт"
        
    def get_vehicle_info(self):
        return f"{super().get_vehicle_info()} - {self.engine_size}л"