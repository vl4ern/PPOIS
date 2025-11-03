from classes.Inventory_classes.Part import Part

class Tire(Part):
    def __init__(self, item_id, name, price, compatible_vehicles, size, season):
        super().__init__(item_id, name, "Автомобильная шина", price, compatible_vehicles)
        self.size = size
        self.season = season
    
    def __str__(self):
        return f"{super().__str__()} - {self.size} {self.season}"