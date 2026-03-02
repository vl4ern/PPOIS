class Device:
    def __init__(self, name:str):
        self.name = name
        self.is_on = False

    def turn_on(self):
        self.is_on = True
        print(f"{self.name} сейчас включен/a")
    
    def turn_off(self):
        self.is_on = False
        print(f"{self.name} сейчас выключен/a")
    
    def __str__(self):
        status = "ON" if self.is_on else "OFF"
        return f"--Device: {self.name} | Status: {status}--"
    


class SmartLight(Device):
    def __init__(self, name, brightness: int=100):
        super().__init__(name)
        self.brightness = brightness
        
    def turn_on(self):
        super().turn_on()
        print(f"{self.name} сейчас включен/a и светит с яркостью {self.brightness}")
    
    def set_brightness(self, level:int):
        if 0 <= level <= 100:
            self.brightness = level
            print(f"Яркость лампочки установлена {self.brightness}.")
        else:
            print("Некорректный ввод, яркость может быть от 0 до 100!!!")



class Thermostat(Device):
    def __init__(self, name, temperature: int = 22):
        super().__init__(name)
        self.temperature = temperature

    def turn_on(self):
        super().turn_on()
        print(f"{self.name} сейчас включен/a и греет воздух до {self.temperature} градусов.")

    def set_temp(self, temp:int):
        if 15 <= temp <= 27:
            self.temperature = temp
        else:
            print("Вы пытаетесь поставить слишком некомфортную температуру!")



class SmartHome:
    def __init__(self, name:str):
        self.name = name
        self.devices = []

    def add_device(self, device):
        self.devices.append(device)
        print(f"{device} добавлено в систему --Умный дом--")

    def activate_scenario(self):
        print("\n---Запуск сценария: 'Я дома'---")
        for gatget in self.devices:
            gatget.turn_on()

    def turn_all_off(self):
        print("Доброй ночи, сценарий выключения всего.")
        for gatget in self.devices:
            gatget.turn_off()

def main():
    home = SmartHome('Мая хата')
    my_smart_light = SmartLight('Люстра')
    my_smart_termostat = Thermostat('Термометр')
    
    my_smart_light.set_brightness(90)
    my_smart_termostat.set_temp(23)

    home.add_device(my_smart_light)
    home.add_device(my_smart_termostat)

    home.activate_scenario()

    home.turn_all_off()    

    #my_smart_termostat.set_temp(value_termostat)
    #my_smart_termostat.turn_on()
    #print(my_smart_termostat)
    #my_smart_termostat.turn_off()
    #print(my_smart_termostat)
    
    #my_smart_light.set_brightness(value_light)
    #my_smart_light.turn_on()
    #print(my_smart_light)
    #my_smart_light.turn_off()
    #print(my_smart_light)


if __name__ == "__main__":
    main()