from __future__ import annotations
from app.facade import ParkingFacade
from app.services.parking_service import CarNotFoundError, PaymentError, SpotOccupiedError


def print_menu() -> None:
    print("=== Автостоянка 78: CLI ===")
    print("1. Показать состояние парковки")
    print("2. Разместить автомобиль")
    print("3. Оплатить парковку")
    print("4. Добавить услугу")
    print("5. Выдать автомобиль")
    print("6. Проверка охраны")
    print("7. Сбросить доход")
    print("0. Выход")


def show_state(facade: ParkingFacade) -> None:
    stats = facade.stats()
    print(f"Название: {stats['name']}")
    print(f"Всего мест: {stats['total_spots']}")
    print(f"Занято: {stats['occupied_spots']}")
    print(f"Свободно: {stats['free_spots']}")
    print(f"Доход: {stats['income']} $")
    print(f"Свободные места: {', '.join(stats['free_spots_list']) if stats['free_spots_list'] else 'нет'}")
    print(f"Рекомендация: {stats['recommendation']}")

    cars = facade.cars_for_view()
    if not cars:
        print("На парковке сейчас нет автомобилей.")
        return

    print("Автомобили на парковке:")
    for car in cars:
        print(
            f"- {car['license_plate']} | {car['model']} | место {car['spot_id']} | "
            f"оплачено: {'да' if car['paid'] else 'нет'}"
        )


def run_cli() -> None:
    facade = ParkingFacade()

    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()

        try:
            if choice == "1":
                show_state(facade)
            elif choice == "2":
                facade.place_car(
                    license_plate=input("Номер автомобиля: "),
                    model=input("Модель: "),
                    year=int(input("Год выпуска: ")),
                    owner=input("Владелец: "),
                    spot_id=input("Место (например, A01): ").strip().upper(),
                )
                print("Автомобиль успешно размещён.")
            elif choice == "3":
                result = facade.pay_for_parking(
                    license_plate=input("Номер автомобиля: "),
                    tariff_id=input("ID тарифа (standard/four_hours/day/three_days): ").strip(),
                )
                print(f"Оплата принята: {result['cost']} $. Тариф: {result['tariff_name']}.")
            elif choice == "4":
                price = facade.add_service(
                    license_plate=input("Номер автомобиля: "),
                    service_id=input("ID услуги (wash/charge/wifi/security): ").strip(),
                )
                print(f"Услуга добавлена. Стоимость: {price} $.")
            elif choice == "5":
                result = facade.remove_car(input("Номер автомобиля: "))
                print(f"Автомобиль {result['license_plate']} выдан, место {result['spot_id']} освобождено.")
            elif choice == "6":
                info = facade.security_info(input("Номер автомобиля: "))
                services = ', '.join(info['services']) if info['services'] else 'нет'
                print(
                    f"Машина {info['license_plate']}, владелец: {info['owner']}, место: {info['spot_id']}, "
                    f"въезд: {info['entry_time']}, охрана: {info['security_status']}, услуги: {services}."
                )
            elif choice == "7":
                facade.reset_income()
                print("Доход успешно обнулён.")
            elif choice == "0":
                print("Выход из программы.")
                break
            else:
                print("Неизвестная команда.")
        except (ValueError, SpotOccupiedError, CarNotFoundError, PaymentError) as error:
            print(f"Ошибка: {error}")
