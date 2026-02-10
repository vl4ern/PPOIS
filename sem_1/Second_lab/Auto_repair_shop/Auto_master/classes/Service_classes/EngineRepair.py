from classes.Service_classes.Service import Service

class EngineRepair(Service):
    def __init__(self, service_id):
        super().__init__(service_id, "Ремонт двигателя", "Капитальный ремонт двигателя", 500.0)
        self.duration_hours = 8.0
    
    def calculate_final_price(self, vehicle):
        return self.base_price