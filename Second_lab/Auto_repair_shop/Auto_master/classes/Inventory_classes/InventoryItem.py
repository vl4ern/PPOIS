from classes.Exceptions.InsufficientPartsException import InsufficientPartsException

class InventoryItem:
    def __init__(self, item_id, name, description, price):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.price = price
        self.quantity = 0
    
    def update_quantity(self, quantity):
        self.quantity = quantity
    
    def reduce_quantity(self, amount):
        if self.quantity < amount:
            raise InsufficientPartsException(f"Недостаточно {self.name}")
        self.quantity -= amount
    
    def __str__(self):
        return f"{self.name} - ${self.price}"