from classes.Person.Mechanic import Mechanic

class Electrician(Mechanic):
    def __init__(self, employee_id, name, salary, certification_level):
        super().__init__(employee_id, name, salary, "Электрик")
        self.certification_level = certification_level
        
    def __str__(self):
        return f"{super().__str__()} - Сертификация: {self.certification_level}"