class Tariff:
    def __init__(self, tariff_id: str, name: str, price_per_hour: float, min_time: int = 1, max_time: int = 24):
        self.tariff_id = tariff_id
        self.name = name
        self.price_per_hour = price_per_hour
        self.min_time = min_time
        self.max_time = max_time

    def calculate_cost(self, duraction:int)->float:
        return round(self.price_per_hour * duraction, 2)
    
    def to_dict(self)->dict:
        return{
            'tariff_id': self.tariff_id,
            'name': self.name,
            'price_per_hour': self.price_per_hour,
            'min_time': self.min_time,
            'max_time': self.max_time
        }
    
    @staticmethod
    def from_dict(data: dict)-> 'Tariff':
        return Tariff(
            tariff_id=data['tariff_id'],
            name=data['name'],
            price_per_hour=data['price_per_hour'],
            min_time=data['min_time'],
            max_time=data['max_time']
        )