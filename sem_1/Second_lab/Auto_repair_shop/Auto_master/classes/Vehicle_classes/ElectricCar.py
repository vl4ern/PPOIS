from classes.Vehicle_classes.Car import Car

class Electric_Car(Car):
    def __init__(self, vin, brand, model, year, body_type, battery_capacity):
        super().__init__(vin, brand, model, year, body_type)
        self.engine_type = "Электрическая машина"
        self.battery_capacity = battery_capacity
        self.charge_level = 100
        
    def charge_battery(self,amount):
        self.charge_level = min(100, self.charge_level + amount)
        
    def get_vehicle_info(self):
        return f"{super().get_vehicle_info()} - Батарея {self.battery_capacity}КВ/ч" 