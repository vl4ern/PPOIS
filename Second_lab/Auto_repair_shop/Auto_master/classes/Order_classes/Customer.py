class Customer:
    def __init__(self, customer_id, name, phone, email):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
        self.email = email
        self.vehicles = []
        self.order_history = []
    
    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)
    
    def add_order_to_history(self, work_order):
        self.order_history.append(work_order)
    
    def __str__(self):
        return f"{self.name} - {self.phone}"