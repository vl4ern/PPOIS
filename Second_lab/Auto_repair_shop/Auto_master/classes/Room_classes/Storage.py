class Storage:
    def __init__(self, storage_id, area, capacity):
        self.storage_id = storage_id
        self.area = area
        self.capacity = capacity
        self.inventory_items = []
    
    def add_item(self, item, quantity):
        self.inventory_items.append((item, quantity))
    
    def __str__(self):
        return f"Склад #{self.storage_id} - {len(self.inventory_items)} позиция"