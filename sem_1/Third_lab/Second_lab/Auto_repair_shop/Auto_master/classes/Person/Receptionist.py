from classes.Person.Employee import Employee

class Receprionist(Employee):
    def __init__(self, employee_id, name, salary, shift):
        super().__init__(employee_id, name, "Регистратор", salary)
        self.shift = shift
        self.appointment = []
        
    def schedule_appointment(self,customer, date_time, service):
        appointment = {
            'customer': customer,
            'date_time' : date_time,
            'service' : service
        }
        self.appointment.append(appointment)
        
    def __str__(self):
        return f"{super().__str__()} - Смена: {self.shift}"