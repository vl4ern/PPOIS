from PPOIS.First_lab.Post_Machine.Rule import Rule

class Program:
    """Класс, представляющий программу машины Поста как набор правил"""
    def __init__(self):
        self.rules = {} 
        self.current_rule = 1  
    
    def add_rule(self, rule):
        """Добавить правило в программу"""
        self.rules[rule.number] = rule
    
    def remove_rule(self, number):
        """Удалить правило из программы"""
        if number in self.rules:
            del self.rules[number]
    
    def get_rule(self, number):
        """Получить правило по номеру"""
        return self.rules.get(number)
    
    def view_rules(self):
        """Просмотреть все правила (соответствует требованию просмотра правил)"""
        return "\n".join(str(rule) for num, rule in sorted(self.rules.items()))
    
    def load_from_stream(self, stream):
        """Загрузить программу (набор правил) из потока"""
        for line in stream:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            try:
                # Формат: номер: условие -> действие_истина; действие_ложь
                parts = line.split(':')
                number = int(parts[0].strip())
                
                actions_part = parts[1].split(';')
                condition_action = actions_part[0].split('->')
                condition = condition_action[0].strip()
                action_true = condition_action[1].strip()
                
                action_false = actions_part[1].split('->')[1].strip()
                
                rule = Rule(number, condition, action_true, action_false)
                self.add_rule(rule)
                
            except (ValueError, IndexError) as e:
                print(f"Ошибка parsing правила: {line}")
                continue
    
    def __str__(self):
        """Строковое представление программы (набора правил)"""
        return self.view_rules()