from datetime import datetime, timedelta

class Warranty:
    def __init__(self, warranty_id, work_order, duration_months):
        self.warranty_id = warranty_id
        self.work_order = work_order
        self.issue_date = datetime.now()
        self.expiry_date = self.issue_date + timedelta(days=duration_months*30)
    
    def is_valid(self):
        return datetime.now() <= self.expiry_date
    
    def __str__(self):
        return f"Гарантия #{self.warranty_id} к {self.expiry_date.strftime('%d.%m.%Y')}"