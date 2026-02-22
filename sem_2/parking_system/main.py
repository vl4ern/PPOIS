import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime
from models.car import Car
from models.parking import Parking
from services.parking_service import PaskingService

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ParkingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.parking = Parking.load_from_file()
        self.service = PaskingService(self.parking)

        self.title("Модель автостоянки")
        self.geometry("1000x1000")
        self.resizable(True, True)

        self.create_widgets()

        self.update_status()

    def create_widgets(self):
    # ========== Верхняя панель ==========
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(fill="x", padx=10, pady=10)

        # Заголовок
        title_label = ctk.CTkLabel(
            self.top_frame,
            text="Автостоянка 78",
            font=("Arial", 24, "bold")
        )
        title_label.pack(padx=20, pady=10)  # ✅ pack

        # Фрейм для статистики (вложенный)
        self.stats_frame = ctk.CTkFrame(self.top_frame)
        self.stats_frame.pack(fill="x", padx=10, pady=5)

        # Статистика - теперь в отдельном фрейме, можно использовать grid
        self.total_label = ctk.CTkLabel(self.stats_frame, text="Всего мест: 0")
        self.total_label.grid(row=0, column=0, padx=10, pady=5)
        
        self.occupied_label = ctk.CTkLabel(self.stats_frame, text="Занято: 0")
        self.occupied_label.grid(row=0, column=1, padx=10, pady=5)
        
        self.free_label = ctk.CTkLabel(self.stats_frame, text="Свободно: 0")
        self.free_label.grid(row=0, column=2, padx=10, pady=5)
        
        self.income_label = ctk.CTkLabel(self.stats_frame, text="Доход: 0 $")
        self.income_label.grid(row=0, column=3, padx=10, pady=5)

        self.reset_income_btn = ctk.CTkButton(
            self.stats_frame,
            text="Сбросить",
            width=80,
            fg_color="#D32F2F",  
            hover_color="#B71C1C",
            command=self.reset_total_income 
        )
        self.reset_income_btn.grid(row=0, column=4, padx=10, pady=5)
        
        
        # ========== Главный контейнер ==========
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Вкладки
        self.tabview = ctk.CTkTabview(self.main_container)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Добавляем вкладки
        self.tab_home = self.tabview.add("Главная")
        self.tab_park = self.tabview.add("Разместить автомобиль")
        self.tab_payment = self.tabview.add("Оплата")
        self.tab_services = self.tabview.add("Услуги")
        self.tab_security = self.tabview.add("Охрана")
        self.tab_traffic = self.tabview.add("Движение")
        self.tab_status = self.tabview.add("Статус парковки")
        
        # Создаем содержимое вкладок
        self.create_home_tab()
        self.create_park_tab()
        self.create_payment_tab()
        self.create_services_tab()
        self.create_security_tab()
        self.create_traffic_tab()
        self.create_status_tab()
        
        # ========== Нижняя панель ==========
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.pack(fill="x", padx=10, pady=5)
        
        status_label = ctk.CTkLabel(
            self.bottom_frame, 
            text="© 2026 Автостоянка 78 | Все права защищены",
            font=("Arial", 10)
        )
        status_label.pack(pady=5)
        
    def update_status(self):
        """Обновление статистики"""
        free_spots_list = self.parking.get_free_spots()
        free_spots_count = len(self.parking.get_free_spots())
        occupied_spots = len(self.parking.get_occupied_spots())
        
        self.total_label.configure(text=f"Всего мест: {len(self.parking.spots)}")
        self.occupied_label.configure(text=f"Занято: {occupied_spots}")
        self.free_label.configure(text=f"Свободно: {free_spots_count}")
        self.income_label.configure(text=f"Доход: {self.parking.total_income:.2f} $")

        if hasattr(self, 'spot_combo'):
            self.spot_combo.configure(free_spots_list)
            current_spot = self.spot_combo.get()
            if not free_spots_list:
                self.spot_combo.set("Нет мест.")
            elif current_spot not in free_spots_list:
                self.spot_combo.set(free_spots_list[0])


    def reset_total_income(self):
        """Обработка нажатия на кнопку сброса дохода"""
        # Спрашиваем подтверждение (защита от случайного клика)
        confirm = messagebox.askyesno(
            "Подтверждение", 
            "Вы уверены, что хотите обнулить счетчик дохода?\n\nЭто действие нельзя отменить!"
        )
        
        if confirm:
            try:
                # 1. Сбрасываем доход через сервис
                self.service.reset_income()
                
                # 2. Сохраняем изменения в файл (чтобы при перезапуске был 0)
                self.parking.save_to_file()
                
                # 3. Обновляем цифры на экране
                self.update_status()
                
                messagebox.showinfo("Успех", "Касса успешно обнулена (проведена инкассация).")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось обнулить доход: {str(e)}")
    
    # ========== Вкладка "Главная" ==========
    def create_home_tab(self):
        """Создание вкладки Главная"""
        
        # Приветствие
        welcome_frame = ctk.CTkFrame(self.tab_home)
        welcome_frame.pack(fill="x", padx=20, pady=20)
        
        welcome_label = ctk.CTkLabel(
            welcome_frame,
            text="Добро пожаловать на автостоянку!",
            font=("Arial", 20, "bold")
        )
        welcome_label.pack(pady=10)
        
        desc_label = ctk.CTkLabel(
            welcome_frame,
            text="У нас всегда есть место для вашего автомобиля",
            font=("Arial", 14)
        )
        desc_label.pack(pady=5)
        
        # Кнопка размещения автомобиля
        park_btn = ctk.CTkButton(
            welcome_frame,
            text="Разместить автомобиль",
            font=("Arial", 16, "bold"),
            height=50,
            command=lambda: self.tabview.set("Разместить автомобиль")
        )
        park_btn.pack(pady=20, padx=50, fill="x")
        
        # Информация о парковке
        info_frame = ctk.CTkFrame(self.tab_home)
        info_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        info_title = ctk.CTkLabel(
            info_frame,
            text="О нашей парковке",
            font=("Arial", 16, "bold")
        )
        info_title.pack(pady=10)
        
        info_text = """Автостоянка 78 предоставляет безопасное и удобное место для парковки вашего автомобиля. Мы предлагаем:"""
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=("Arial", 12),
            justify="left"
        )
        info_label.pack(padx=20, pady=10)
    
    # ========== Вкладка "Разместить автомобиль" ==========
    def create_park_tab(self):
        """Создание вкладки Размещение автомобиля"""
        
        # Проверка свободных мест
        free_spots = self.parking.get_free_spots()
        
        if len(free_spots) == 0:
            no_spots_label = ctk.CTkLabel(
                self.tab_park,
                text="❌ К сожалению, на парковке нет свободных мест.\nПопробуйте позже.",
                font=("Arial", 16, "bold"),
                text_color="red"
            )
            no_spots_label.pack(pady=50)
            return
        
        # Форма ввода данных
        form_frame = ctk.CTkFrame(self.tab_park)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            form_frame,
            text="Разместить автомобиль на парковке",
            font=("Arial", 18, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Поля ввода
        fields = [
            ("Номер автомобиля:", "license_plate"),
            ("Модель автомобиля:", "model"),
            ("Год выпуска:", "year"),
            ("Фамилия владельца:", "owner"),
        ]
        
        self.park_entries = {}
        
        for i, (label_text, var_name) in enumerate(fields, start=1):
            label = ctk.CTkLabel(form_frame, text=label_text, font=("Arial", 12))
            label.grid(row=i, column=0, sticky="e", padx=10, pady=10)
            
            entry = ctk.CTkEntry(form_frame, width=300)
            entry.grid(row=i, column=1, sticky="w", padx=10, pady=10)
            self.park_entries[var_name] = entry
        
        # Выбор места
        spot_label = ctk.CTkLabel(form_frame, text="Выберите парковочное место:", font=("Arial", 12))
        spot_label.grid(row=5, column=0, sticky="e", padx=10, pady=10)
        
        self.spot_combo = ctk.CTkComboBox(
            form_frame,
            values=free_spots,
            width=300
        )
        self.spot_combo.grid(row=5, column=1, sticky="w", padx=10, pady=10)
        self.spot_combo.set(free_spots[0])  # Устанавливаем первое место по умолчанию
        
        # Кнопки
        button_frame = ctk.CTkFrame(form_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=30)
        
        place_btn = ctk.CTkButton(
            button_frame,
            text="Разместить автомобиль",
            font=("Arial", 14, "bold"),
            command=self.place_car
        )
        place_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Отмена",
            command=self.clear_park_form
        )
        cancel_btn.pack(side="left", padx=10)
    
    def place_car(self):
        """Обработка размещения автомобиля"""
        try:
            # Получаем данные из формы
            license_plate = self.park_entries['license_plate'].get().strip()
            model = self.park_entries['model'].get().strip()
            year = self.park_entries['year'].get().strip()
            owner = self.park_entries['owner'].get().strip()
            spot_id = self.spot_combo.get()
            
            # Валидация
            if not all([license_plate, model, year, owner]):
                messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля!")
                return
            
            try:
                year_int = int(year)
                if year_int < 1900 or year_int > 2026:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", "Год выпуска должен быть числом от 1900 до 2026!")
                return
            
            # Создаем автомобиль
            car = Car(license_plate, model, year_int, owner)
            
            # Размещаем на парковке
            self.service.place_car(car, spot_id)
            
            # Сохраняем
            self.parking.save_to_file()
            
            # Обновляем статистику
            self.update_status()
            
            messagebox.showinfo(
                "Успех", 
                f"Автомобиль {license_plate} успешно размещен на месте {spot_id}!\n\n"
                f"Перейдите на вкладку 'Оплата' для оплаты парковки."
            )
            
            # Очищаем форму
            self.clear_park_form()
            
            # Переключаем на вкладку оплаты
            self.tabview.set("Оплата")
            
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    
    def clear_park_form(self):
        """Очистка формы размещения"""
        for entry in self.park_entries.values():
            entry.delete(0, "end")
        
        free_spots = self.parking.get_free_spots()
        if free_spots:
            self.spot_combo.configure(values=free_spots)
            self.spot_combo.set(free_spots[0])
    
    # ========== Вкладка "Оплата" ==========
    def create_payment_tab(self):
        """Создание вкладки Оплата"""
        
        frame = ctk.CTkFrame(self.tab_payment)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            frame,
            text="Оплата парковки",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=20)
        
        # Выбор автомобиля
        select_frame = ctk.CTkFrame(frame)
        select_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(select_frame, text="Номер автомобиля:").pack(side="left", padx=10)
        
        self.payment_license_entry = ctk.CTkEntry(select_frame, width=200)
        self.payment_license_entry.pack(side="left", padx=10)
        
        check_btn = ctk.CTkButton(
            select_frame,
            text="Проверить",
            command=self.check_car_for_payment
        )
        check_btn.pack(side="left", padx=10)
        
        # Информация об автомобиле
        self.car_info_frame = ctk.CTkFrame(frame)
        self.car_info_frame.pack(fill="x", padx=20, pady=10)
        self.car_info_frame.pack_forget()  # Скрываем пока
        
        self.car_info_label = ctk.CTkLabel(self.car_info_frame, text="", font=("Arial", 12))
        self.car_info_label.pack(pady=10)
        
        # Выбор тарифа
        tariff_frame = ctk.CTkFrame(frame)
        tariff_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(tariff_frame, text="Выберите тариф:", font=("Arial", 14, "bold")).pack(pady=10)
        
        self.tariff_var = ctk.StringVar()
        self.tariff_buttons = []
        
        for tariff_id, tariff in self.parking.tariffs.items():
            btn = ctk.CTkRadioButton(
                tariff_frame,
                text=f"{tariff.name} - {float(tariff.price_per_hour):.0f} $",
                variable=self.tariff_var,
                value=tariff_id
            )
            btn.pack(anchor="w", padx=20, pady=5)
            self.tariff_buttons.append(btn)
        
        # Кнопки оплаты
        pay_frame = ctk.CTkFrame(frame)
        pay_frame.pack(pady=20)
        
        pay_btn = ctk.CTkButton(
            pay_frame,
            text="Оплатить",
            font=("Arial", 14, "bold"),
            command=self.process_payment
        )
        pay_btn.pack(side="left", padx=10)
        
        back_btn = ctk.CTkButton(pay_frame, text="Назад", command=lambda: self.tabview.set("Главная"))
        back_btn.pack(side="left", padx=10)
    
    def check_car_for_payment(self):
        """Проверка автомобиля для оплаты"""
        license_plate = self.payment_license_entry.get().strip()
        
        if not license_plate:
            messagebox.showerror("Ошибка", "Введите номер автомобиля!")
            return
        
        if license_plate not in self.parking.cars:
            messagebox.showerror("Ошибка", f"Автомобиль {license_plate} не найден на парковке!")
            return
        
        car = self.parking.cars[license_plate]
        
        info_text = f"Автомобиль: {car.model} ({car.year})\n"
        info_text += f"Владелец: {car.owner}\n"
        info_text += f"Место: {car.spot_id}\n"
        info_text += f"Время прибытия: {car.entry_time.strftime('%d.%m.%Y %H:%M')}"
        
        self.car_info_label.configure(text=info_text)
        self.car_info_frame.pack(fill="x", padx=20, pady=10)
        
        # Выбираем первый тариф по умолчанию
        if self.parking.tariffs:
            self.tariff_var.set(list(self.parking.tariffs.keys())[0])
    
    def process_payment(self):
        """Обработка оплаты"""
        license_plate = self.payment_license_entry.get().strip()
        
        if not license_plate:
            messagebox.showerror("Ошибка", "Введите номер автомобиля!")
            return
        
        tariff_id = self.tariff_var.get()
        
        if not tariff_id:
            messagebox.showerror("Ошибка", "Выберите тариф!")
            return
        
        try:
            payment_info = self.service.pay_for_parking(license_plate, tariff_id)
            self.parking.save_to_file()
            
            messagebox.showinfo(
                "Оплата успешна",
                f"Стоимость: {payment_info['cost']} $\n"
                f"Тариф: {payment_info['tariff_name']}\n"
                f"Время: {payment_info['duration']} часов"
            )
            
            # Переключаем на вкладку услуг
            self.tabview.set("Услуги")
            
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    
    # ========== Вкладка "Услуги" ==========
    def create_services_tab(self):
        """Создание вкладки Услуги"""
        
        frame = ctk.CTkFrame(self.tab_services)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            frame,
            text="Дополнительные услуги",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=20)
        
        # Выбор автомобиля
        select_frame = ctk.CTkFrame(frame)
        select_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(select_frame, text="Номер автомобиля:").pack(side="left", padx=10)
        
        self.service_license_entry = ctk.CTkEntry(select_frame, width=200)
        self.service_license_entry.pack(side="left", padx=10)
        
        check_btn = ctk.CTkButton(
            select_frame,
            text="Проверить",
            command=self.check_car_for_services
        )
        check_btn.pack(side="left", padx=10)
        
        # Список услуг
        services_frame = ctk.CTkFrame(frame)
        services_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(services_frame, text="Доступные услуги:", font=("Arial", 14, "bold")).pack(pady=10)
        
        self.service_vars = {}
        
        for service_id, service in self.parking.services.items():
            var = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(
                services_frame,
                text=f"{service.name} - {service.price} $",
                variable=var
            )
            checkbox.pack(anchor="w", padx=20, pady=5)
            self.service_vars[service_id] = var
        
        # Кнопки
        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(pady=20)
        
        order_btn = ctk.CTkButton(
            btn_frame,
            text="Заказать услуги",
            font=("Arial", 14, "bold"),
            command=self.order_services
        )
        order_btn.pack(side="left", padx=10)
        
        back_btn = ctk.CTkButton(btn_frame, text="Назад", command=lambda: self.tabview.set("Главная"))
        back_btn.pack(side="left", padx=10)
    
    def check_car_for_services(self):
        """Проверка автомобиля для услуг"""
        license_plate = self.service_license_entry.get().strip()
        
        if not license_plate:
            messagebox.showerror("Ошибка", "Введите номер автомобиля!")
            return
        
        if license_plate not in self.parking.cars:
            messagebox.showerror("Ошибка", f"Автомобиль {license_plate} не найден!")
            return
        
        messagebox.showinfo("Успех", f"Автомобиль {license_plate} найден. Выберите услуги.")
    
    def order_services(self):
        """Заказ услуг"""
        license_plate = self.service_license_entry.get().strip()
        
        if not license_plate:
            messagebox.showerror("Ошибка", "Введите номер автомобиля!")
            return
        
        if license_plate not in self.parking.cars:
            messagebox.showerror("Ошибка", f"Автомобиль {license_plate} не найден!")
            return
        
        selected_services = [
            service_id for service_id, var in self.service_vars.items() if var.get()
        ]
        
        if not selected_services:
            messagebox.showwarning("Внимание", "Выберите хотя бы одну услугу!")
            return
        
        total_cost = 0
        for service_id in selected_services:
            try:
                cost = self.service.add_service_to_car(license_plate, service_id)
                total_cost += cost
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
                return
        
        self.parking.save_to_file()
        
        messagebox.showinfo(
            "Услуги заказаны",
            f"Заказано {len(selected_services)} услуг(и)\n"
            f"Общая стоимость: {total_cost} $"
        )

        for var in self.service_vars.values():
            var.set(False)
    
    # ========== Вкладка "Охрана" ==========
    def create_security_tab(self):
        """Создание вкладки Охрана"""
        
        frame = ctk.CTkFrame(self.tab_security)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            frame,
            text="Проверка безопасности",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=20)
        
        # Выбор автомобиля
        select_frame = ctk.CTkFrame(frame)
        select_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(select_frame, text="Номер автомобиля:").pack(side="left", padx=10)
        
        self.security_license_entry = ctk.CTkEntry(select_frame, width=200)
        self.security_license_entry.pack(side="left", padx=10)
        
        check_btn = ctk.CTkButton(
            select_frame,
            text="Проверить",
            command=self.check_security
        )
        check_btn.pack(side="left", padx=10)
        
        # Результат проверки
        self.security_result_frame = ctk.CTkFrame(frame)
        self.security_result_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.security_result_frame.pack_forget()
        
        self.security_result_text = ctk.CTkLabel(
            self.security_result_frame,
            text="",
            font=("Arial", 12),
            justify="left"
        )
        self.security_result_text.pack(pady=20, padx=20)
    
    def check_security(self):
        """Проверка безопасности"""
        license_plate = self.security_license_entry.get().strip()
        
        if not license_plate:
            messagebox.showerror("Ошибка", "Введите номер автомобиля!")
            return
        
        try:
            security_info = self.service.check_security(license_plate)
            
            result_text = "✅ ПРОВЕРКА БЕЗОПАСНОСТИ ПРОЙДЕНА ✅\n\n"
            result_text += f"Номер автомобиля: {security_info['license_plate']}\n"
            result_text += f"Владелец: {security_info['owner']}\n"
            result_text += f"Парковочное место: {security_info['spot_id']}\n"
            result_text += f"Время прибытия: {security_info['entry_time']}\n"
            result_text += f"Статус охраны: {security_info['security_status']}\n\n"
            
            if security_info['services']:
                result_text += "Дополнительные услуги:\n"
                for service in security_info['services']:
                    result_text += f"  • {service}\n"
            
            self.security_result_text.configure(text=result_text)
            self.security_result_frame.pack(fill="both", expand=True, padx=20, pady=10)
            
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    
    # ========== Вкладка "Движение" ==========
    def create_traffic_tab(self):
        """Создание вкладки Управление движением"""
        
        frame = ctk.CTkFrame(self.tab_traffic)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            frame,
            text="Управление движением на парковке",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=20)
        
        # Кнопка оптимизации
        optimize_btn = ctk.CTkButton(
            frame,
            text="Оптимизировать движение",
            font=("Arial", 14, "bold"),
            height=40,
            command=self.optimize_traffic
        )
        optimize_btn.pack(pady=20)
        
        # Результат
        self.traffic_result_frame = ctk.CTkFrame(frame)
        self.traffic_result_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.traffic_result_frame.pack_forget()
        
        self.traffic_result_text = ctk.CTkLabel(
            self.traffic_result_frame,
            text="",
            font=("Arial", 12),
            justify="left"
        )
        self.traffic_result_text.pack(pady=20, padx=20)
    
    def optimize_traffic(self):
        """Оптимизация движения"""
        traffic_info = self.service.optimize_traffic()
        
        result_text = "📊 СТАТИСТИКА ДВИЖЕНИЯ НА ПАРКОВКЕ 📊\n\n"
        result_text += f"Всего мест: {traffic_info['total_spots']}\n"
        result_text += f"Занято: {traffic_info['occupied_spots']}\n"
        result_text += f"Свободно: {traffic_info['free_spots']}\n"
        result_text += f"Заполненность: {traffic_info['occupancy_rate']}%\n\n"
        
        result_text += "РЕКОМЕНДАЦИЯ:\n"
        result_text += f"  {traffic_info['recommendation']}"
        
        self.traffic_result_text.configure(text=result_text)
        self.traffic_result_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # ========== Вкладка "Статус парковки" ==========
    def create_status_tab(self):
        """Создание вкладки Статус парковки"""
        
        frame = ctk.CTkFrame(self.tab_status)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            frame,
            text="Статус парковки",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=10)
        
        # Кнопки действий
        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        refresh_btn = ctk.CTkButton(
            btn_frame,
            text="Обновить",
            command=self.refresh_status
        )
        refresh_btn.pack(side="left", padx=5)
        
        export_btn = ctk.CTkButton(
            btn_frame,
            text="Экспортировать данные",
            command=self.export_data
        )
        export_btn.pack(side="left", padx=5)
        
        # Таблица автомобилей
        table_frame = ctk.CTkFrame(frame)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Создаем таблицу с помощью Treeview (стандартный tkinter)
        columns = ("license", "model", "year", "owner", "spot", "paid", "services")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Настройка заголовков
        self.tree.heading("license", text="Номер")
        self.tree.heading("model", text="Модель")
        self.tree.heading("year", text="Год")
        self.tree.heading("owner", text="Владелец")
        self.tree.heading("spot", text="Место")
        self.tree.heading("paid", text="Оплачено")
        self.tree.heading("services", text="Услуги")
        
        # Настройка ширины колонок
        self.tree.column("license", width=100)
        self.tree.column("model", width=150)
        self.tree.column("year", width=60)
        self.tree.column("owner", width=120)
        self.tree.column("spot", width=80)
        self.tree.column("paid", width=80)
        self.tree.column("services", width=200)
        
        # Добавляем прокрутку
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Кнопки управления автомобилем
        car_btn_frame = ctk.CTkFrame(frame)
        car_btn_frame.pack(fill="x", padx=20, pady=10)
        
        remove_btn = ctk.CTkButton(
            car_btn_frame,
            text="Убрать автомобиль",
            command=self.remove_selected_car
        )
        remove_btn.pack(side="left", padx=5)
        
        # Заполняем таблицу
        self.refresh_status()
    
    def refresh_status(self):
        """Обновление статуса парковки"""
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Заполняем данными
        for car in self.parking.cars.values():
            services = ", ".join([
                self.parking.services[sid].name 
                for sid in car.services 
                if sid in self.parking.services
            ]) if car.services else "—"
            
            self.tree.insert("", "end", values=(
                car.license,
                car.model,
                car.year,
                car.owner,
                car.spot_id or "—",
                "Да" if car.paid else "Нет",
                services
            ))
        
        # Обновляем статистику
        self.update_status()
    
    def remove_selected_car(self):
        """Убрать выбранный автомобиль"""
        selected = self.tree.selection()
        
        if not selected:
            messagebox.showwarning("Внимание", "Выберите автомобиль для удаления!")
            return
        
        item = self.tree.item(selected[0])
        license_plate = str(item['values'][0])
        
        try:
            result = self.service.remove_car(license_plate)
            self.parking.save_to_file()
            
            messagebox.showinfo(
                "Успех",
                f"Автомобиль {license_plate} покинул парковку!\n"
                f"Место {result['spot_id']} освобождено."
            )
            
            self.refresh_status()
            
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    
    def export_data(self):
        """Экспортировать данные"""
        try:
            filename = f"parking_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            self.parking.save_to_file(filename)
            
            messagebox.showinfo(
                "Экспорт успешен",
                f"Данные экспортированы в файл:\n{filename}"
            )
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


# Запуск приложения
if __name__ == "__main__":
    app = ParkingApp()
    app.mainloop()