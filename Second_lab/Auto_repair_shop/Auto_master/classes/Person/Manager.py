from classes.Person.Employee import Employee

class Manager(Employee):
    def __init__(self, employee_id, name, salary, department):
        super().__init__(employee_id, name, "Менеджер", salary)
        self.department = department
        
    def __str__(self):
        return f"{super().__str__()} - {self.department}"