from classes.Inventory_classes.InventoryItem import InventoryItem

class Tool(InventoryItem):
    def __init__(self, item_id, name, description, price, tool_type):
        super().__init__(item_id, name, description, price)
        self.tool_type = tool_type
        self.is_available = True
    
    def __str__(self):
        return f"{super().__str__()} - {self.tool_type}"