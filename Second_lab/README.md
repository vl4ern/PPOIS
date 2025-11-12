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