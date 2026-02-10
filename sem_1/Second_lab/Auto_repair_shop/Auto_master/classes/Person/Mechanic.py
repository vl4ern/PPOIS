from classes.Person.Employee import Employee
from classes.Exceptions.EmployeeNotAvailableException import EmployeeNotAvailableException

class Mechanic(Employee):
    def __init__(self, employee_id, name, salary, specialization):
        super().__init__(employee_id, name, "Механик", salary)
        self.specialization = specialization
        self.current_vechicle = None
    
    def assign_vehicle(self, vechicle):
        if not self.is_avaible:
            raise EmployeeNotAvailableException(f"Механик {self.name} не готов к работе.")
        self.current_vechicle = vechicle
        self.is_avalable = False
        
    def __str__(self):
        return f"{super().__str__()} - {self.specialization}"