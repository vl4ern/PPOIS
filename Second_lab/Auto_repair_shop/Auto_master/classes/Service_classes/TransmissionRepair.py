from classes.Service_classes.Service import Service

class TransmissionRepair(Service):
    def __init__(self, service_id):
        super().__init__(service_id, "Ремонт трансмиссии", "Ремонт трансмиссии", 400.0)
        self.duration_hours = 6.0
    
    def calculate_final_price(self, vehicle):
        return self.base_price