class Tape:
    # Лента Машины Поста
    def __init__(self, initial_data=""):
        self.cells = list(initial_data) if initial_data else ['0']
        self.position = 0
        
    # ПОлучение значния
    def get_current(self):
        if 0 <= self.position < len(self.cells):
            return self.cells[self.position]
        return '0'
    
    # Проверяем на диапазон
    def set_current(self, value):
        if 0 <= self.position < len(self.cells):
            self.cells[self.position] = value
        else:
            # Расширяем ленту если нужно
            if self.position < 0:
                self.cells = ['0'] * (-self.position) + self.cells
                self.position = 0
            else:
                self.cells.extend(['0'] * (self.position - len(self.cells) + 1))
            self.cells[self.position] = value
            
            # Функции передвижение
    def move_left(self):
        self.position -= 1
        if self.position < 0:
            self.cells.insert(0, '0')
            self.position = 0
    
    def move_right(self):
        self.position += 1
        if self.position >= len(self.cells):
            self.cells.append('0')
    
    def load_from_stream(self, stream):
        data = stream.readline().strip()
        self.cells = list(data) if data else ['0']
        self.position = 0
    
    def __str__(self):
        result = []
        for i, cell in enumerate(self.cells):
            if i == self.position:
                result.append(f"[{cell}]")
            else:
                result.append(f" {cell} ")
        return "".join(result)