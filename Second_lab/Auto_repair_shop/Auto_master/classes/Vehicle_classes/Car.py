from classes.Vehicle_classes.Vehicle import Vehicle

class Car(Vehicle):
    def __init__(self, vin, brand, model, year, body_type):
        super().__init__(vin, brand, model, year)
        self.body_type = body_type
        self.engine_type = "Бензин"
        
    def get_vehicle_info(self):
        return f"{super().get_vehicle_info()} - {self.body_type}"