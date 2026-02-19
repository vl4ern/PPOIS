from datetime import datetime
from typing import Optional, List

class Car:
    """Класс под автомобиль"""

    def __init__(self, license: str, model: str, year: int, owner: str):
        self.license = license
        self.model = model
        self.year = year
        self.owner = owner
        self.entry_time: Optional[datetime] = None
        self.spot_id: Optional[str] = None
        self.paid: bool = False
        self.paid_time: int = 0  #время оплаты в часах
        self.services: List[str] = []

    def to_dict(self)->dict:
        return{
            'license': self.license,
            'model': self.model,
            'year': self.year,
            'owner': self.owner,
            'entry_time': self.entry_time.isoformat() if self.entry_time else None,
            'spot_id': self.spot_id,
            'paid': self.paid,
            'paid_duration': self.paid_time,
            'services': self.services
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Car':
        car = Car(
            license=data['license'],
            model=data['model'],
            year=data['year'],
            owner=data['owner']
        )
        if data['entry_time']:
            car.entry_time = datetime.fromisoformat(data['entry_time'])
        car.spot_id=data['spod_id']
        car.paid=data['paid']
        car.paid_time=data['paid_time']
        car.services=data['services']
        return car