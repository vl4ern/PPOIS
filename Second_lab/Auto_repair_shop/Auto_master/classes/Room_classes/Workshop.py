from classes.Exceptions.WorkshopFullException import WorkshopFullException

class Workshop:
    def __init__(self, workshop_id, area, capacity):
        self.workshop_id = workshop_id
        self.area = area
        self.capacity = capacity
        self.current_vehicles = []
    
    def add_vehicle(self, vehicle):
        if len(self.current_vehicles) >= self.capacity:
            raise WorkshopFullException("Мастерская переполнена.")
        self.current_vehicles.append(vehicle)
    
    def __str__(self):
        return f"Мастерская #{self.workshop_id} - {len(self.current_vehicles)}/{self.capacity}"