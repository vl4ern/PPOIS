from classes.Service_classes.Service import Service

class OilChange(Service):
    def __init__(self, service_id):
        super().__init__(service_id, "Замена масла", "Замена масла и фильтра", 50.0)
        self.oil_type = "Synthetic"
    
    def calculate_final_price(self, vehicle):
        if hasattr(vehicle, 'максимальная загрузка'):  # Trucks are more expensive
            return self.base_price * 1.5
        return self.base_price