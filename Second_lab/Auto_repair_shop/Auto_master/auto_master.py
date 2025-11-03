from classes.Vehicle_classes.Vehicle import Vehicle
from classes.Vehicle_classes.Car import Car
from classes.Vehicle_classes.Truck import Track
from classes.Vehicle_classes.ElectricCar import Electric_Car
from classes.Vehicle_classes.Motorcycle import Motorcycle
from classes.Person.Employee import Employee
from classes.Person.Mechanic import Mechanic
from classes.Person.Manager import Manager
from classes.Person.Electrician import Electrician
from classes.Person.Receptionist import Receprionist
from classes.Person.Accountant import Accountant
from classes.Service_classes.Service import Service
from classes.Service_classes import OilChange
from classes.Service_classes.BrakeService import BrakeService
from classes.Service_classes import ElectricalRepair
from classes.Service_classes.EngineRepair import EngineRepair
from classes.Service_classes.TransmissionRepair import TransmissionRepair
from classes.Service_classes import TireService
from classes.Service_classes import DiagnosticService
#from classes.Inventory_classes import InventoryItem
from classes.Inventory_classes import Part
#from classes.Inventory_classes.Tool import Tool
from classes.Inventory_classes.OilFilter import OilFilter
from classes.Inventory_classes.BrakePads import BrakePads
from classes.Inventory_classes.EngineOil import EngineOil
from classes.Inventory_classes.Battery import Battery
from classes.Inventory_classes.Tire import Tire
from classes.Order_classes.WorkOrder import WorkOrder
from classes.Order_classes.Invoice import Invoice
from classes.Order_classes.Customer import Customer
from classes.Order_classes.Payment import Payment
from classes.Order_classes.Warranty import Warranty
from classes.Room_classes.Workshop import Workshop
from classes.Room_classes.Parking import Parking
from classes.Room_classes.Storage import Storage
from classes.Room_classes.Office import Office
from classes.Exceptions.InvalidVehicleDataException import InvalidVehicleDataException
from classes.Exceptions.PaymentFailedException import PaymentFailedException

class AutoMaster:
    def __init__(self):
        self.customers = []
        self.employees = []
        self.work_orders = []
        self.inventory = []
        self.facilities = []
        self._initialize_data()
    
    def _initialize_data(self):
        """Инициализация предопределенных данных"""
        # Сотрудники
        self.employees = [
            Mechanic(1, "Иван Петров", 50000.0, "Двигатели"),
            Mechanic(2, "Алексей Смирнов", 48000.0, "Тормоза"),
            Electrician(3, "Дмитрий Козлов", 55000.0, "Уровень 2"),
            Manager(4, "Мария Иванова", 60000.0, "Обслуживание"),
            Receprionist(5, "Анна Сидорова", 35000.0, "Дневная"),
            Accountant(6, "Ольга Николаева", 45000.0, "CPA")
        ]
        
        # Запчасти
        self.inventory = [
            OilFilter(1, "Фильтр масляный", 15.0, ["Honda", "Toyota"], "Синтетический"),
            BrakePads(2, "Колодки тормозные", 120.0, ["Honda", "Toyota"], "Керамика"),
            EngineOil(3, "Масло моторное", 45.0, "5W-30", "Синтетическое"),
            Battery(4, "Аккумулятор", 100.0, ["Honda", "Toyota"], 12, 60),
            Tire(5, "Шина летняя", 80.0, ["Honda", "Toyota"], "195/65R15", "Лето")
        ]
        
        # Помещения
        self.facilities = [
            Workshop(1, 100, 5),
            Parking(2, 200, 20),
            Storage(3, 50, 1000),
            Office(4, 30, "Главный офис")
        ]
    
    def create_customer(self, name, phone, email):
        customer_id = len(self.customers) + 1
        customer = Customer(customer_id, name, phone, email)
        self.customers.append(customer)
        return customer
    
    def create_vehicle(self, vehicle_type, vin, brand, model, year, **kwargs):
        if vehicle_type == "car":
            return Car(vin, brand, model, year, kwargs.get('body_type', 'седан'))
        elif vehicle_type == "truck":
            return Track(vin, brand, model, year, kwargs.get('max_load', 1000))
        elif vehicle_type == "electric":
            return Electric_Car(vin, brand, model, year, kwargs.get('body_type', 'седан'), 
                             kwargs.get('battery_capacity', 50.0))
        elif vehicle_type == "motorcycle":
            return Motorcycle(vin, brand, model, year, kwargs.get('engine_size', 600))
        else:
            raise InvalidVehicleDataException("Неизвестный тип ТС")
    
    def choose_services_interactive(self):
        services = []
        available_services = {
            1: OilChange.OilChange(1),
            2: BrakeService(2),
            3: ElectricalRepair.ElectricalRepair(3),
            4: EngineRepair(4),
            5: TransmissionRepair(5),
            6: TireService.TireService(6),
            7: DiagnosticService.DiagnosticService(7)
        }
        
        print("Доступные услуги:")
        for key, service in available_services.items():
            print(f"{key}. {service.name} - ${service.base_price}")
        
        while True:
            try:
                choice = input("Выберите услугу (1-7) или 'done' для завершения: ")
                if choice.lower() == 'done':
                    break
                service_num = int(choice)
                if service_num in available_services:
                    services.append(available_services[service_num])
                    print(f"✅ Добавлена услуга: {available_services[service_num].name}")
                else:
                    print("❌ Неверный выбор")
            except ValueError:
                print("❌ Введите число или 'done'")
        
        return services
    
    def create_work_order(self, customer, vehicle, services):
        order_id = len(self.work_orders) + 1
        work_order = WorkOrder(order_id, vehicle, customer.name)
        
        for service in services:
            work_order.add_service(service)
        
        # Назначаем первого доступного механика
        available_mechanics = [e for e in self.employees if isinstance(e, Mechanic) and e.is_avalable]
        if available_mechanics:
            work_order.assign_mechanic(available_mechanics[0])
        
        self.work_orders.append(work_order)
        customer.add_order_to_history(work_order)
        return work_order
    
    def create_invoice(self, work_order):
        invoice_id = len(self.work_orders) + 1
        return Invoice(invoice_id, work_order)
    
    def process_payment_interactive(self, invoice):
        print(f"\n💳 Оплата услуг (${invoice.work_order.total_cost:.2f}):")
        payment_methods = {"1": "Наличные", "2": "Кредитная карта", "3": "Банковский перевод"}
        
        for key, method in payment_methods.items():
            print(f"{key}. {method}")
        
        while True:
            payment_choice = input("Выберите метод оплаты: ")
            if payment_choice in payment_methods:
                try:
                    amount = float(input("Введите сумму оплаты: "))
                    invoice.process_payment(payment_methods[payment_choice], amount)
                    print("✅ Оплата прошла успешно!")
                    break
                except PaymentFailedException as e:
                    print(f"❌ Ошибка оплаты: {e}")
                except ValueError:
                    print("❌ Введите корректную сумму")
            else:
                print("❌ Неверный выбор метода оплаты")
    
    def create_warranty(self, work_order, months):
        warranty_id = len(self.work_orders) + 1
        return Warranty(warranty_id, work_order, months)
    
    def display_order_summary(self, customer, vehicle, work_order, invoice, warranty):
        print("\n" + "=" * 50)
        print("🎉 ЗАКАЗ УСПЕШНО ВЫПОЛНЕН!")
        print("=" * 50)
        print(f"Клиент: {customer.name}")
        print(f"Транспорт: {vehicle}")
        print(f"Механик: {work_order.assigned_mechanic.name if work_order.assigned_mechanic else 'Не назначен'}")
        print(f"Услуги: {', '.join([s.name for s in work_order.services])}")
        print(f"Итоговая стоимость: ${work_order.total_cost:.2f}")
        print(f"Статус оплаты: {'Оплачено' if invoice.is_paid else 'Не оплачено'}")
        print(f"Гарантия до: {warranty.expiry_date.strftime('%d.%m.%Y')}")
        print("=" * 50)