from typing import Optional

class ParkingSpot:
    def __init__(self, spot_id: str):
        self.spot_id = spot_id
        self.is_occupied: bool = False
        self.car_plate: Optional[str] = None
        self.tariff_id: str = 'standart'

    def to_dict(self)->dict:
        return{
            'spot_id': self.spot_id,
            'is_occupied': self.is_occupied,
            'car_plate': self.car_plate,
            'tariff_id': self.tariff_id
        }
    
    @staticmethod
    def from_dict(data: dict)->'ParkingSpot':
        spot = ParkingSpot(data['spot_id'])
        spot.is_occupied = data['is_occupited']
        spot.car_plate = data['car_plate']
        spot.tariff_id = data['tariff_id']
        return spot