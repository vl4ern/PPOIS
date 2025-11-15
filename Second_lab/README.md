# README: Автомастерская (Car repair shop)

- Классы: 51
- Поля: 154
- Уникальные поведения: 104
- Ассоциации: 33
- Исключения: 12

## Исключения (12)
Находятся в директории Exceptions

- AutomasterException — базовое исключение.
- VehicleNotFoundException — транспортное средство не найдено.
- InvalidVehicleDataException — некорректные данные о транспортном средстве.
- WorkshopFullException — превышена вместимость мастерской.
- EmployeeNotAvailableException — сотрудник недоступен.
- InsufficientPartsException — недостаточно запчастей.
- PaymentFailedException — ошибка при оплате.
- InvalidServiceException — некорректный тип услуги.
- DiagnosticFailedException — ошибка диагностики.
- QualityControlFailedException — ошибка контроля качества.
- VehicleNotFoundException - ошибка поиска трансорта
- WarrantyExpiredException - ошибка в случае истекшей гарантии
- WorkshopFullException - ошибка при невозможно операции в мастерской

## Классы
Формат: Имя_класса Поля Методы -> Ассоциации (связанные классы/модули)

### Vehicle_classes

Vehicle 6 4 -> Part, Service, Diagnostic
- Поля: vin, brand, model, year, mileage, last_service_date 
- Методы: update_mileage, get_vehicle_info, __init__, __str__

Track 5 3 -> Vehicle
- Поля: vin, brand, model, year, max_load
- Методы: load_cargo, get_vehicle_info, __init__

Motorcycle 5 2 -> Vehicle
- Поля: vin, brand, model, year, engine_size
- Методы: get_vehicle_info, __init__

ElectricCar 6 3 -> Car
- Поля: vin, brand, model, year, body_type, battery_capacity
- Методы: charge_battery, get_vehicle_info, __init__

Car 5 2 -> Vehicle
- Поля: vin, brand, model, year, body_type
- Методы: get_vehicle_info, __init__

### Service_classes

BrakeService 3 2 -> Service
- Поля: service_id, brake_pads_needed, base_price
- Методы: calculate_final_price, __init__

DiagnosticService 3 2 -> Service
- Поля: service_id, duration_hours, base_price
- Методы: calculate_final_price, __init__

ElectricalRepair 3 2 -> Service
- Поля: service_id, complexity, base_price
- Методы: calculate_final_price, __init__

EngineRepair 3 2 -> Service
- Поля: service_id, duration_hours, base_price
- Методы: calculate_final_price, __init__

OilChange 4 2 -> Service
- Поля: service_id, oil_type, vehicle, base_price
- Методы: calculate_final_price, __init__

Service 5 3 -> Part, Vehicle
- Поля: service_id, name, description, base_price, duration_hours
- Методы: calculate_final_price, __init__, __str__

TireService 3 2 -> Service
- Поля: service_id, includes_balance, base_price
- Методы: calculate_final_price, __init__

TransmissionRepair 3 2 -> Service
- Поля: service_id, duration_hours, base_price
- Методы: calculate_final_price, __init__

### Inventory_classes

Battery 6 2 -> Part
- Поля: item_id, name, price, compatible_vehicles, voltage, capacity
- Методы: __init__, __str__

BrakePads 5 2 -> Part
- Поля: item_id, name, price, compatible_vehicles, material
- Методы: __init__, __str__

EngineOil 5 2 -> InventoryItem
- Поля: item_id, name, price, viscosity, oil_type
- Методы: __init__, __str__

InventoryItem 6 2 -> Service, Vehicle
- Поля: item_id, name, description, price, quantity, amount
- Методы: reduce_quantity, update_quantity

OilFilter 5 1 -> Part
- Поля: item_id, name, price, compatible_vehicles, filter_type
- Методы: __init__, __str__

Part 5 1 -> InventoryItem
- Поля: item_id, name, description, price, compatible_vehicles
- Методы: is_compatible_with

Tire 6 2 -> Part
- Поля: item_id, name, price, compatible_vehicles, size, season
- Методы: __init__, __str__

Tool 6 2 -> InventoryItem
- Поля: item_id, name, description, price, tool_type, is_available
- Методы: __init__, __str__

### Orser_classes

Customer 6 4 -> Automaster, Vehicle
- Поля: customer_id, name, phone, email, vehicles, order_history
- Методы: __init__, __str__, add_vehicle, add_order_to_history

Invoice 5 3 -> Payment, WorkOrder, Customer
- Поля: invoice_id, work_order, issue_date, is_paid, payment_method
- Методы: __init__, __str__, process_payment

Payment -> Invoice, Customer
- Поля: payment_id, amount, payment_method, payment_date, status
- Методы: __init__, __str__

Warranty -> WorkOrder
- Поля: warranty_id, work_order, duration_months, issue_date, expiry_date
- Методы: __init__, __str__, is_valid

WorkOrder 8 6 -> Vehicle, Customer, Service
- Поля: order_id, vehicle, customer_name, creation_date, status, services, assigned_mechanic, total_cost
- Методы: __init__, __str__, complete_order, _calculate_total_cost, assign_mechanic, add_service

### Person

Accountant 5 2 -> Employee
- Поля: self, employee_id, name, salary, certification
- Методы: __init__, __str__

Electrician 4 2 -> Mechanic
- Поля: employee_id, name, salary, certification_level
- Методы: __init__, __str__

Employee 5 2 
- Поля: employee_id, name, position, salary, is_avalable
- Методы: __init__, __str__

Manager 4 2 -> Employee
- Поля: employee_id, name, salary, department
- Методы: __init__, __str__

Mechanic 6 3 -> Employee, Vehicle
- Поля: employee_id, name, salary, specialization, current_vechicle, is_avalable
- Методы: __init__, __str__, assign_vehicle

Receprionist 8 3 -> Employee
- Поля: employee_id, name, salary, shift, customer, date_time, service, appointment
- Методы: __init__, __str__, schedule_appointment

### Room_classes

Office 4 3 -> Employee
- Поля: office_id, area, department, employees
- Методы: __init__, __str__, add_employee

Parking 4 3 -> Vehicle
- Поля: parking_id, area, capacity, parked_vehicles
- Методы: __init__, __str__, park_vehicle

Storage 5 3 -> InventoryItem
- Поля: storage_id, area, capacity, inventory_items, quantity
- Методы: __init__, __str__, add_item

Workshop 5 3 -> Vehicle
- Поля: workshop_id, area, capacity, vehicle, current_vehicles
- Методы: __init__, __str__, add_vehicle

### Auto master

from classes.Service_classes import TireService
AutoMaster 23 10 -> Car, Track, Electric_Car, Motorcycle, Mechanic, Manager, Electrician, Receprionist, Accountant, OilChange, BrakeService, ElectricalRepair, EngineRepair, TransmissionRepair, TireService, DiagnosticService, OilFilter, BrakePads, EngineOil, Battery, Tire, WorkOrder, Invoice, Customer, Warranty, Workshop, Parking, Storage, Office
- Поля: customers, work_orders, employees, inventory, facilities, _initialize_data, customer_id, customer, vehicle_type, vin, brand, model, year, services, available_services, key, service_num, order_id, work_order, invoice_id, payment_methods, payment_choice, warranty_id
- Методы: display_order_summary, create_warranty, process_payment_interactive, create_invoice, create_work_order, choose_services_interactive, create_vehicle, create_customer, _initialize_data, init