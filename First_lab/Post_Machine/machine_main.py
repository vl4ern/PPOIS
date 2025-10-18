import sys
from machine_post import Post_Machine

def main():
    if len(sys.argv) < 2:
        print("Использование: python post_machine.py <файл> [-log]")
        sys.exit(1)
    
    filename = sys.argv[1]
    log_mode = len(sys.argv) > 2 and sys.argv[2] == '-log'
    
    try:
        # Создаем и инициализируем машину Поста
        machine = Post_Machine()
        
        with open(filename, 'r', encoding='utf-8') as f:
            # Первая строка - начальное состояние ленты
            machine.load_tape_from_stream(f)
            # Остальные строки - программа (набор правил)
            machine.load_program_from_stream(f)
        
        print("Начальное состояние:")
        print(machine)
        print("\nЗагруженные правила:")
        print(machine.program.view_rules())
        print()
        
        if log_mode:
            # Пошаговое выполнение с выводом после каждого шага
            step = 1
            while machine.execute_step():
                print(f"После шага {step}:")
                print(machine)
                step += 1
                print()
        else:
            # Выполнение всей программы
            machine.execute_all()
        
        print("\nФинальное состояние:")
        print(machine)
        
        
        # проверка на существование файла с правилами
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()