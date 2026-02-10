class Parking:
    def __init__(self, parking_id, area, capacity):
        self.parking_id = parking_id
        self.area = area
        self.capacity = capacity
        self.parked_vehicles = []
    
    def park_vehicle(self, vehicle):
        if len(self.parked_vehicles) < self.capacity:
            self.parked_vehicles.append(vehicle)
            return True
        return False
    
    def __str__(self):
        return f"Стоянка #{self.parking_id} - {len(self.parked_vehicles)}/{self.capacity}"