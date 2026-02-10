from classes.Service_classes.Service import Service

class ElectricalRepair(Service):
    def __init__(self, service_id):
        super().__init__(service_id, "Ремонт электрооборудования", "Ремонт электропроводки", 200.0)
        self.complexity = "Средняя"
    
    def calculate_final_price(self, vehicle):
        if self.complexity == "High":
            return self.base_price * 1.5
        return self.base_price