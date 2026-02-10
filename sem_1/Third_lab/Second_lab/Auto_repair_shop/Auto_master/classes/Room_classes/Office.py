class Office:
    def __init__(self, office_id, area, department):
        self.office_id = office_id
        self.area = area
        self.department = department
        self.employees = []
    
    def add_employee(self, employee):
        self.employees.append(employee)
    
    def __str__(self):
        return f"Офис #{self.office_id} - {self.department}"