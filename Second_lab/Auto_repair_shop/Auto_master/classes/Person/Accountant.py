from classes.Person.Employee import Employee

class Accountant(Employee):
    def __init__(self, employee_id, name, salary, certification):
        super().__init__(employee_id, name, "Бухгалтер", salary)
        self.certification = certification
        
    def __str__(self):
        return f"{super().__str__()} - {self.certification}"