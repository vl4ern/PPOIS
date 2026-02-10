from classes.Inventory_classes.InventoryItem import InventoryItem

class EngineOil(InventoryItem):
    def __init__(self, item_id, name, price, viscosity, oil_type):
        super().__init__(item_id, name, "Моторное масло", price)
        self.viscosity = viscosity
        self.oil_type = oil_type
    
    def __str__(self):
        return f"{super().__str__()} - {self.viscosity} {self.oil_type}"