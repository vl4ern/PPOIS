from classes.Service_classes.Service import Service

class TireService(Service):
    def __init__(self, service_id):
        super().__init__(service_id, "Шиномонтажный сервис", "Замена и балансировка шин", 80.0)
        self.includes_balance = True
    
    def calculate_final_price(self, vehicle):
        return self.base_price