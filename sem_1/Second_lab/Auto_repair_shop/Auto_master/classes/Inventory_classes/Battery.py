from classes.Inventory_classes.Part import Part

class Battery(Part):
    def __init__(self, item_id, name, price, compatible_vehicles, voltage, capacity):
        super().__init__(item_id, name, "Батарея", price, compatible_vehicles)
        self.voltage = voltage
        self.capacity = capacity
    
    def __str__(self):
        return f"{super().__str__()} - {self.voltage}Вт {self.capacity}Ач"