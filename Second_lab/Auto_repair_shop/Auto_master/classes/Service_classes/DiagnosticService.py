from classes.Service_classes.Service import Service

class DiagnosticService(Service):
    def __init__(self, service_id):
        super().__init__(service_id, "Диагностика", "Компьютерная диагностика", 60.0)
        self.duration_hours = 0.5
    
    def calculate_final_price(self, vehicle):
        return self.base_price