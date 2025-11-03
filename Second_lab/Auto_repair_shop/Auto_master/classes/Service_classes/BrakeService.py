from classes.Service_classes.Service import Service

class BrakeService(Service):
    def __init__(self, service_id):
        super().__init__(service_id, "Ремонт тормозов", "Замена тормозных колодок и дисков", 120.0)
        self.brake_pads_needed = True
    
    def calculate_final_price(self, vehicle):
        base = self.base_price
        if self.brake_pads_needed:
            base += 80.0
        return base