from datetime import datetime
from typing import Optional, List

class Car:
    """Класс для автомобиля"""

    def __init__(self, license = str, model = str, year = int, owner = str):
        self.license = license
        self.model = model
        self.year = year