from classes.Inventory_classes.InventoryItem import InventoryItem

class Part(InventoryItem):
    def __init__(self, item_id, name, description, price, compatible_vehicles):
        super().__init__(item_id, name, description, price)
        self.compatible_vehicles = compatible_vehicles
        
        # Исправление: убираем форматирование для чисел, работаем со строковыми ID
        # Просто добавляем префикс "PN" к существующему item_id
        self.part_number = f"PN{item_id}"
    
    def is_compatible_with(self, vehicle):
        return vehicle.brand in self.compatible_vehicles
    
    def __str__(self):
        return f"{super().__str__()} - Совместимость: {', '.join(self.compatible_vehicles)}"