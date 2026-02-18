class Service:
    def __init__(self, service_id: str, name: str, price: float, description: str =""):
        self.service_id = service_id
        self.name = name
        self.price = price
        self.description = description

    def to_dict(self)->dict:
        return{
            'service_id': self.service_id,
            'name': self.name,
            'price': self.price,
            'description': self.description
        }
    
    @staticmethod
    def from_dict(data: dict)->'Service':
        return Service(
            service_id=data['service_id'],
            name=data['name'],
            price=data['price'],
            description=data.get('description', '')
        )