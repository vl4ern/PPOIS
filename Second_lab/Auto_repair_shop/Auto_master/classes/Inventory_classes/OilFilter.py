from classes.Inventory_classes.Part import Part

class OilFilter(Part):
    def __init__(self, item_id, name, price, compatible_vehicles, filter_type):
        super().__init__(item_id, name, "Масляный фильтр", price, compatible_vehicles)
        self.filter_type = filter_type
    
    def __str__(self):
        return f"{super().__str__()} - {self.filter_type}"