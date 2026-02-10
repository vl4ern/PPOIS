class Employee:
    def __init__(self, employee_id, name, position, salary):
        self.employee_id = employee_id
        self.name = name
        self.position = position
        self.salary = salary
        self.is_avalable = True
        
    def __str__(self):
        return f"{self.name} - {self.position}"