class Rule:
    def __init__(self, number, condition, action_true, action_false):
        self.number = number
        self.condition = condition  # '1' - метка есть, '0' - метки нет
        self.action_true = action_true
        self.action_false = action_false
    
    def execute(self, tape):
        current_value = tape.get_current()
        
        if current_value == self.condition:
            return self.action_true
        else:
            return self.action_false
    
    def __str__(self):
        return f"{self.number}: {self.condition} -> {self.action_true}; !{self.condition} -> {self.action_false}"
