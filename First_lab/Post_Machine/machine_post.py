from PPOIS.First_lab.Post_Machine.Tape import Tape
from PPOIS.First_lab.Post_Machine.Program import Program

class Post_Machine:
    def __init__(self):
        self.tape = Tape()
        self.program = Program()
        self.halted = False
        self.step_count = 0
    
    # потокавая ленты загрузка
    def load_tape_from_stream(self, stream):
        self.tape.load_from_stream(stream)
    
    # потоковая загрузка программы и правил
    def load_program_from_stream(self, stream):
        self.program.load_from_stream(stream)
    
    # один шаг
    def execute_step(self):
        if self.halted:
            return False
        
        current_rule = self.program.get_rule(self.program.current_rule)
        if not current_rule:
            self.halted = True
            return False
        
        action = current_rule.execute(self.tape)
        self.step_count += 1
        
        # Обработка действий
        if action == 'V':  # Поставить метку
            self.tape.set_current('1')
            self.program.current_rule += 1
        elif action == 'X':  # Стереть метку
            self.tape.set_current('0')
            self.program.current_rule += 1
        elif action == 'R':  # Движение вправо
            self.tape.move_right()
            self.program.current_rule += 1
        elif action == 'L':  # Движение влево
            self.tape.move_left()
            self.program.current_rule += 1
        elif action.startswith('?'): 
            try:
                self.program.current_rule = int(action[1:])
            except(ValueError, IndexError):
                self.halted = True
        elif action == '!':  # Остановка
            self.halted = True
        else:  # Простой переход на правило
            try:
                self.program.current_rule = int(action)
            except ValueError:
                self.halted = True
        
        return True
    
    # выполнение всех возможных шагов
    def execute_all(self):
        while self.execute_step():
            pass
    
    # возвращение текующего состояния машины
    def get_state(self):
        return {
            'step': self.step_count,
            'current_rule': self.program.current_rule,
            'tape': str(self.tape),
            'halted': self.halted
        }
    
    # строковый формат предствавления состояния
    def __str__(self):
        state = self.get_state()
        return (f"Шаг: {state['step']}, "
                f"Правило: {state['current_rule']}, "
                f"Лента: {state['tape']}, "
                f"Остановлена: {state['halted']}")
