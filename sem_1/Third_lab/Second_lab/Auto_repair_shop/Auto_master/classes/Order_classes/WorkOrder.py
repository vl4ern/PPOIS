from datetime import datetime

class WorkOrder:
    def __init__(self, order_id, vehicle, customer_name):
        self.order_id = order_id
        self.vehicle = vehicle
        self.customer_name = customer_name
        self.creation_date = datetime.now()
        self.status = "Созданный"
        self.services = []
        self.assigned_mechanic = None
        self.total_cost = 0.0
    
    def add_service(self, service):
        self.services.append(service)
        self._calculate_total_cost()
    
    def assign_mechanic(self, mechanic):
        self.assigned_mechanic = mechanic
        self.status = "В ходе выполнения"
        mechanic.is_available = False
    
    def _calculate_total_cost(self):
        self.total_cost = sum(service.calculate_final_price(self.vehicle) for service in self.services)
    
    def complete_order(self):
        self.status = "Завершенный"
        if self.assigned_mechanic:
            self.assigned_mechanic.is_available = True
    
    def __str__(self):
        return f"Заказ #{self.order_id} - {self.customer_name} - ${self.total_cost:.2f}"