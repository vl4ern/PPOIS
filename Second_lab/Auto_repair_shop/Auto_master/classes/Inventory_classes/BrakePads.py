from classes.Inventory_classes.Part import Part

class BrakePads(Part):
    def __init__(self, item_id, name, price, compatible_vehicles, material):
        super().__init__(item_id, name, "Тормозные колодки", price, compatible_vehicles)
        self.material = material
    
    def __str__(self):
        return f"{super().__str__()} - {self.material}"