from Auto_master.auto_master import AutoMaster

def main():
    automaster = AutoMaster()
    
    print("🚗 Добро пожаловать в Автомастерскую! 🛠️")
    print("=" * 50)
    
    # Создание клиента
    print("\n📝 Регистрация клиента:")
    name = input("Ваше полное имя: ")
    phone = input("Ваш телефон: ")
    email = input("Ваш email: ")
    
    customer = automaster.create_customer(name, phone, email)
    print(f"✅ Клиент создан: {customer}")
    
    # Создание транспортного средства
    print("\n🚗 Информация о транспортном средстве:")
    print("Доступные типы ТС: car, truck, electric, motorcycle")
    vehicle_type = input("Тип ТС: ").lower()
    vin = input("VIN номер (17 символов): ")
    brand = input("Марка: ")
    model = input("Модель: ")
    year = int(input("Год выпуска: "))
    
    additional_params = {}
    if vehicle_type == "car":
        additional_params['body_type'] = input("Тип кузова: ")
    elif vehicle_type == "truck":
        additional_params['max_load'] = float(input("Грузоподъемность (кг): "))
    elif vehicle_type == "electric":
        additional_params['body_type'] = input("Тип кузова: ")
        additional_params['battery_capacity'] = float(input("Емкость батареи (кВтч): "))
    elif vehicle_type == "motorcycle":
        additional_params['engine_size'] = float(input("Объем двигателя (cc): "))
    
    try:
        vehicle = automaster.create_vehicle(vehicle_type, vin, brand, model, year, **additional_params)
        customer.add_vehicle(vehicle)
        print(f"✅ Транспортное средство создано: {vehicle}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return
    
    # Выбор услуг
    print("\n🔧 Выбор услуг:")
    services = automaster.choose_services_interactive()
    
    if not services:
        print("❌ Не выбрано ни одной услуги")
        return
    
    # Создание заказа
    work_order = automaster.create_work_order(customer, vehicle, services)
    print(f"✅ Заказ создан: {work_order}")
    
    # Создание и оплата счета
    invoice = automaster.create_invoice(work_order)
    print(f"\n💰 Счет создан: {invoice}")
    
    # Оплата
    automaster.process_payment_interactive(invoice)
    
    # Завершение заказа
    work_order.complete_order()
    
    # Создание гарантии
    warranty = automaster.create_warranty(work_order, 12)
    print(f"✅ Гарантия создана на 12 месяцев")
    
    # Вывод итогов
    automaster.display_order_summary(customer, vehicle, work_order, invoice, warranty)

if __name__ == "__main__":
    main()