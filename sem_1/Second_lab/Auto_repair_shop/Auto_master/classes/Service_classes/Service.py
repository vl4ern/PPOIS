class Service:
    def __init__(self, service_id,name,description,base_price):
        self.service_id = service_id
        self.name = name
        self.description = description
        self.base_price = base_price
        self.duration_hours = 1.0
        
    def calculate_final_price(self, vehicle):
        return self.base_price
    
    def __str__(self):
        return f"{self.name} - ${self.base_price}"