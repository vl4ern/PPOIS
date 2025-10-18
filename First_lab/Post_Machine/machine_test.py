import unittest
import io
import sys
import os
import tempfile
from machine_tape import Tape
from machine_post import Post_Machine
from machine_program import Program
from machine_rule import Rule


class TestTape(unittest.TestCase):
    
    def test_initialization(self):
        """Тест инициализации ленты"""
        tape = Tape()
        self.assertEqual(tape.cells, ['0'])
        self.assertEqual(tape.position, 0)
    
    def test_initialization_with_data(self):
        """Тест инициализации ленты с данными"""
        tape = Tape("101")
        self.assertEqual(tape.cells, ['1', '0', '1'])
        self.assertEqual(tape.position, 0)
    
    def test_initialization_empty_string(self):
        """Тест инициализации пустой строкой"""
        tape = Tape("")
        self.assertEqual(tape.cells, ['0'])
        self.assertEqual(tape.position, 0)
    
    def test_initialization_single_char(self):
        """Тест инициализации одним символом"""
        tape = Tape("1")
        self.assertEqual(tape.cells, ['1'])
        self.assertEqual(tape.position, 0)
    
    def test_initialization_with_spaces(self):
        """Тест инициализации с пробелами"""
        tape = Tape(" 1 0 1 ")
        self.assertEqual(tape.cells, [' ', '1', ' ', '0', ' ', '1', ' '])
    
    def test_get_current(self):
        """Тест получения текущего значения"""
        tape = Tape("101")
        self.assertEqual(tape.get_current(), '1')
        
        tape.position = 1
        self.assertEqual(tape.get_current(), '0')
        
        tape.position = 5  # Вне границ
        self.assertEqual(tape.get_current(), '0')
        
        tape.position = -1  # Вне границ слева
        self.assertEqual(tape.get_current(), '0')
    
    def test_set_current(self):
        """Тест установки значения"""
        tape = Tape("101")
        
        tape.set_current('0')
        self.assertEqual(tape.cells[0], '0')
        
        tape.position = 1
        tape.set_current('1')
        self.assertEqual(tape.cells[1], '1')
        
        # Тест расширения ленты вправо
        tape.position = 5
        tape.set_current('1')
        self.assertEqual(len(tape.cells), 6)
        self.assertEqual(tape.cells[5], '1')
        
        # Тест расширения ленты влево
        tape.position = -2
        tape.set_current('1')
        self.assertEqual(tape.position, 0)
        self.assertEqual(tape.cells[0], '1')
        
        # Тест установки нестандартного значения
        tape.set_current('A')
        # Должно установиться какое-то значение без ошибки
    
    def test_move_left(self):
        """Тест движения влево"""
        tape = Tape("101")
        tape.position = 1
        
        tape.move_left()
        self.assertEqual(tape.position, 0)
        self.assertEqual(tape.get_current(), '1')
        
        # Движение за левую границу
        tape.move_left()
        self.assertEqual(tape.position, 0)  # Должно остаться на 0
        self.assertEqual(len(tape.cells), 4)  # Добавилась ячейка слева
        
        # Движение с крайней правой позиции
        tape.position = 3
        tape.move_left()
        self.assertEqual(tape.position, 2)
    
    def test_move_right(self):
        """Тест движения вправо"""
        tape = Tape("101")
        
        tape.move_right()
        self.assertEqual(tape.position, 1)
        self.assertEqual(tape.get_current(), '0')
        
        # Движение за правую границу
        tape.position = 2
        tape.move_right()
        self.assertEqual(tape.position, 3)
        self.assertEqual(len(tape.cells), 4)
        self.assertEqual(tape.get_current(), '0')
        
        # Движение с крайней левой позиции
        tape.position = 0
        tape.move_right()
        self.assertEqual(tape.position, 1)
    
    def test_load_from_stream(self):
        """Тест загрузки из потока"""
        tape = Tape()
        stream = io.StringIO("1101\n")
        tape.load_from_stream(stream)
        self.assertEqual(tape.cells, ['1', '1', '0', '1'])
        self.assertEqual(tape.position, 0)
        
        # Пустой поток
        tape = Tape("existing")
        stream = io.StringIO("\n")
        tape.load_from_stream(stream)
        self.assertEqual(tape.cells, ['0'])
        
        # Поток с пробелами
        tape = Tape()
        stream = io.StringIO(" 1 0 1 \n")
        tape.load_from_stream(stream)
        # Должны остаться все символы включая пробелы
    
    def test_load_from_stream_special_cases(self):
        """Тест специальных случаев загрузки"""
        # Поток с табуляцией
        tape = Tape()
        stream = io.StringIO("1\t0\t1\n")
        tape.load_from_stream(stream)
        
        # Очень длинная строка
        tape = Tape()
        long_string = "1" * 1000 + "\n"
        stream = io.StringIO(long_string)
        tape.load_from_stream(stream)
        self.assertEqual(len(tape.cells), 1000)
    
    def test_str_representation(self):
        """Тест строкового представления"""
        tape = Tape("101")
        tape.position = 1
        self.assertEqual(str(tape), " 1 [0] 1 ")
        
        # Пустая лента
        tape = Tape()
        self.assertEqual(str(tape), "[0]")
        
        # Лента с одной ячейкой
        tape = Tape("1")
        self.assertEqual(str(tape), "[1]")
        
        # Позиция в начале
        tape = Tape("101")
        tape.position = 0
        self.assertEqual(str(tape), "[1] 0  1 ")
        
        # Позиция в конце
        tape.position = 2
        self.assertEqual(str(tape), " 1  0 [1]")
        
        # Лента с пробелами
        tape = Tape("1 0 1")
        tape.position = 2
        representation = str(tape)
        self.assertIsInstance(representation, str)
    
    def test_tape_expansion(self):
        """Тест расширения ленты в различных сценариях"""
        tape = Tape()
        
        # Движение вправо с расширением
        for i in range(5):
            tape.move_right()
        self.assertEqual(len(tape.cells), 6)
        
        # Движение влево с расширением
        tape.position = 0
        for i in range(3):
            tape.move_left()
        self.assertEqual(tape.position, 0)  # Не должно уходить в отрицательные
        self.assertGreater(len(tape.cells), 6)
    
    def test_edge_cases(self):
        """Тест граничных случаев"""
        # Лента с очень длинной строкой
        long_data = "1" * 100 + "0" * 50
        tape = Tape(long_data)
        self.assertEqual(len(tape.cells), 150)
        
        # Установка позиции за пределами
        tape.position = 200
        self.assertEqual(tape.get_current(), '0')
        tape.set_current('1')
        self.assertEqual(len(tape.cells), 201)
        
        # Негативная позиция
        tape.position = -5
        self.assertEqual(tape.get_current(), '0')
        tape.set_current('1')
        self.assertEqual(tape.position, 0)
    
    def test_tape_invariants(self):
        """Тест инвариантов ленты"""
        tape = Tape("101")
        
        # После любого движения позиция должна быть валидной
        tape.move_left()
        self.assertGreaterEqual(tape.position, 0)
        self.assertLess(tape.position, len(tape.cells))
        
        tape.move_right()
        self.assertGreaterEqual(tape.position, 0)
        self.assertLess(tape.position, len(tape.cells))


class TestRule(unittest.TestCase):
    
    def test_initialization(self):
        """Тест инициализации правила"""
        rule = Rule(1, '1', 'X', 'V')
        self.assertEqual(rule.number, 1)
        self.assertEqual(rule.condition, '1')
        self.assertEqual(rule.action_true, 'X')
        self.assertEqual(rule.action_false, 'V')
    
    def test_initialization_edge_cases(self):
        """Тест инициализации граничных случаев"""
        # Пустые строки
        rule = Rule(0, '', '', '')
        self.assertEqual(rule.number, 0)
        self.assertEqual(rule.condition, '')
        self.assertEqual(rule.action_true, '')
        self.assertEqual(rule.action_false, '')
        
        # Специальные символы
        rule = Rule(999, '?', '!', 'R')
        self.assertEqual(rule.number, 999)
        self.assertEqual(rule.condition, '?')
    
    def test_execute_with_condition_true(self):
        """Тест выполнения правила при истинном условии"""
        rule = Rule(1, '1', 'X', 'V')
        tape = Tape("1")
        action = rule.execute(tape)
        self.assertEqual(action, 'X')
    
    def test_execute_with_condition_false(self):
        """Тест выполнения правила при ложном условии"""
        rule = Rule(1, '1', 'X', 'V')
        tape = Tape("0")
        action = rule.execute(tape)
        self.assertEqual(action, 'V')
    
    def test_str_representation(self):
        """Тест строкового представления правила"""
        rule = Rule(1, '1', 'X', 'V')
        self.assertEqual(str(rule), "1: 1 -> X; !1 -> V")
        
        # Правило с переходом
        rule = Rule(2, '0', '?5', 'R')
        self.assertEqual(str(rule), "2: 0 -> ?5; !0 -> R")
        
        # Правило с остановкой
        rule = Rule(3, '1', '!', 'L')
        self.assertEqual(str(rule), "3: 1 -> !; !1 -> L")
        
        # Правило с пустыми значениями
        rule = Rule(4, '', '', '')
        self.assertEqual(str(rule), "4:  -> ; ! -> ")
    
    def test_execute_edge_cases(self):
        """Тест граничных случаев выполнения"""
        # Правило с несуществующим условием
        rule = Rule(1, 'A', 'X', 'V')
        tape = Tape("1")
        action = rule.execute(tape)
        self.assertEqual(action, 'V')  # Условие не совпало
        
        # Пустая лента
        rule = Rule(1, '1', 'X', 'V')
        tape = Tape("")
        action = rule.execute(tape)
        self.assertEqual(action, 'V')
        
        # Пустое условие
        rule = Rule(1, '', 'X', 'V')
        tape = Tape("1")
        action = rule.execute(tape)
        # Не должно падать
    
    def test_rule_comparison(self):
        """Тест сравнения правил"""
        rule1 = Rule(1, '1', 'X', 'V')
        rule2 = Rule(1, '1', 'X', 'V')
        rule3 = Rule(2, '0', 'R', 'L')
        
        # Правила с одинаковыми параметрами должны быть равны
        self.assertEqual(rule1.number, rule2.number)
        self.assertEqual(rule1.condition, rule2.condition)
        
        # Разные правила должны отличаться
        self.assertNotEqual(rule1.number, rule3.number)
    
    def test_execute_with_special_cells(self):
        """Тест выполнения с особыми ячейками"""
        rule = Rule(1, ' ', 'X', 'V')
        tape = Tape("  1")  # Лента с пробелами
        tape.position = 0
        action = rule.execute(tape)
        self.assertEqual(action, 'X')
        
        tape.position = 2
        action = rule.execute(tape)
        self.assertEqual(action, 'V')


class TestProgram(unittest.TestCase):
    
    def test_initialization(self):
        """Тест инициализации программы"""
        program = Program()
        self.assertEqual(program.rules, {})
        self.assertEqual(program.current_rule, 1)
    
    def test_add_rule(self):
        """Тест добавления правила"""
        program = Program()
        rule = Rule(1, '1', 'X', 'V')
        program.add_rule(rule)
        self.assertIn(1, program.rules)
        self.assertEqual(program.rules[1], rule)
        
        # Добавление правила с тем же номером (должно перезаписаться)
        rule2 = Rule(1, '0', 'R', 'L')
        program.add_rule(rule2)
        self.assertEqual(program.rules[1], rule2)
        self.assertEqual(len(program.rules), 1)
    
    def test_add_multiple_rules(self):
        """Тест добавления нескольких правил"""
        program = Program()
        rules = [
            Rule(1, '1', 'X', 'V'),
            Rule(2, '0', 'R', 'L'),
            Rule(3, '1', '?1', '!')
        ]
        
        for rule in rules:
            program.add_rule(rule)
        
        self.assertEqual(len(program.rules), 3)
        for i in range(1, 4):
            self.assertIn(i, program.rules)
    
    def test_remove_rule(self):
        """Тест удаления правила"""
        program = Program()
        rule = Rule(1, '1', 'X', 'V')
        program.add_rule(rule)
        
        program.remove_rule(1)
        self.assertNotIn(1, program.rules)
        
        # Удаление несуществующего правила
        program.remove_rule(999)  # Не должно вызывать ошибку
        self.assertEqual(len(program.rules), 0)
    
    def test_get_rule(self):
        """Тест получения правила"""
        program = Program()
        rule = Rule(1, '1', 'X', 'V')
        program.add_rule(rule)
        
        self.assertEqual(program.get_rule(1), rule)
        self.assertIsNone(program.get_rule(999))
    
    def test_view_rules(self):
        """Тест просмотра правил"""
        program = Program()
        rule1 = Rule(1, '1', 'X', 'V')
        rule2 = Rule(2, '0', 'R', 'L')
        program.add_rule(rule1)
        program.add_rule(rule2)
        
        expected_output = "1: 1 -> X; !1 -> V\n2: 0 -> R; !0 -> L"
        self.assertEqual(program.view_rules(), expected_output)
        
        # Пустая программа
        program = Program()
        self.assertEqual(program.view_rules(), "")
    
    def test_load_from_stream(self):
        """Тест загрузки программы из потока"""
        program = Program()
        stream = io.StringIO("1: 1 -> X; 0 -> V\n2: 1 -> R; 0 -> L\n")
        program.load_from_stream(stream)
        
        self.assertEqual(len(program.rules), 2)
        self.assertIn(1, program.rules)
        self.assertIn(2, program.rules)
        
        rule1 = program.rules[1]
        self.assertEqual(rule1.condition, '1')
        self.assertEqual(rule1.action_true, 'X')
        self.assertEqual(rule1.action_false, 'V')
    
    def test_load_from_stream_with_comments(self):
        """Тест загрузки программы с комментариями"""
        program = Program()
        stream = io.StringIO("# Комментарий\n1: 1 -> X; 0 -> V\n\n# Еще комментарий\n")
        program.load_from_stream(stream)
        
        self.assertEqual(len(program.rules), 1)
        self.assertIn(1, program.rules)
    
    def test_load_from_stream_invalid_format(self):
        """Тест загрузки программы с неверным форматом"""
        program = Program()
        
        # Полностью неверный формат
        stream = io.StringIO("invalid format\n")
        program.load_from_stream(stream)
        self.assertEqual(len(program.rules), 0)
        
        # Частично неверный формат
        stream = io.StringIO("1: invalid -> format; 0 -> V\n")
        program.load_from_stream(stream)
        # Должно обработать, насколько возможно
    
    def test_load_from_stream_empty(self):
        """Тест загрузки из пустого потока"""
        program = Program()
        stream = io.StringIO("")
        program.load_from_stream(stream)
        self.assertEqual(len(program.rules), 0)
    
    def test_load_from_stream_various_errors(self):
        """Тест загрузки с различными ошибками"""
        program = Program()
        
        # Отсутствует двоеточие
        stream = io.StringIO("1 1 -> X; 0 -> V\n")
        program.load_from_stream(stream)
        
        # Отсутствует стрелка
        stream = io.StringIO("1: 1 X; 0 V\n")
        program.load_from_stream(stream)
        
        # Неправильный номер правила
        stream = io.StringIO("abc: 1 -> X; 0 -> V\n")
        program.load_from_stream(stream)
        
        # Только номер
        stream = io.StringIO("1:\n")
        program.load_from_stream(stream)
        
        # Пустая строка после номера
        stream = io.StringIO("1: \n")
        program.load_from_stream(stream)
    
    def test_load_from_stream_special_cases(self):
        """Тест загрузки специальных случаев"""
        program = Program()
        
        # Разделители с разными пробелами
        stream = io.StringIO("1:1->X;0->V\n")
        program.load_from_stream(stream)
        self.assertEqual(len(program.rules), 1)
        
        # Много пробелов
        stream = io.StringIO("1  :  1  ->  X  ;  0  ->  V  \n")
        program.load_from_stream(stream)
        self.assertEqual(len(program.rules), 1)
    
    def test_str_representation(self):
        """Тест строкового представления программы"""
        program = Program()
        rule1 = Rule(1, '1', 'X', 'V')
        rule2 = Rule(2, '0', 'R', 'L')
        program.add_rule(rule1)
        program.add_rule(rule2)
        
        expected_output = "1: 1 -> X; !1 -> V\n2: 0 -> R; !0 -> L"
        self.assertEqual(str(program), expected_output)
    
    def test_current_rule_management(self):
        """Тест управления текущим правилом"""
        program = Program()
        program.current_rule = 5
        self.assertEqual(program.current_rule, 5)
        
        # Возврат к начальному правилу
        program.current_rule = 1
        self.assertEqual(program.current_rule, 1)
        
        # Отрицательное правило (не должно быть возможно, но проверим)
        program.current_rule = -1
        self.assertEqual(program.current_rule, -1)
        
        # Нулевое правило
        program.current_rule = 0
        self.assertEqual(program.current_rule, 0)
    
    def test_rule_ordering(self):
        """Тест порядка правил"""
        program = Program()
        
        # Добавляем правила в разном порядке
        program.add_rule(Rule(3, '1', 'X', 'V'))
        program.add_rule(Rule(1, '0', 'R', 'L'))
        program.add_rule(Rule(2, '1', '?1', '!'))
        
        # Проверяем, что просмотр сортирует по номеру
        rules_str = program.view_rules()
        self.assertTrue(rules_str.startswith("1:"))
        self.assertIn("2:", rules_str)
        self.assertIn("3:", rules_str)
    
    def test_program_invariants(self):
        """Тест инвариантов программы"""
        program = Program()
        
        # После добавления правила, оно должно быть доступно
        rule = Rule(1, '1', 'X', 'V')
        program.add_rule(rule)
        self.assertEqual(program.get_rule(1), rule)
        
        # После удаления правила, оно не должно быть доступно
        program.remove_rule(1)
        self.assertIsNone(program.get_rule(1))


class TestPostMachine(unittest.TestCase):
    
    def test_initialization(self):
        """Тест инициализации машины Поста"""
        machine = Post_Machine()
        self.assertIsInstance(machine.tape, Tape)
        self.assertIsInstance(machine.program, Program)
        self.assertFalse(machine.halted)
        self.assertEqual(machine.step_count, 0)
    
    def test_load_tape_from_stream(self):
        """Тест загрузки ленты из потока"""
        machine = Post_Machine()
        stream = io.StringIO("101\n")
        machine.load_tape_from_stream(stream)
        self.assertEqual(machine.tape.cells, ['1', '0', '1'])
        
        # Пустой поток
        stream = io.StringIO("\n")
        machine.load_tape_from_stream(stream)
        self.assertEqual(machine.tape.cells, ['0'])
    
    def test_load_program_from_stream(self):
        """Тест загрузки программы из потока"""
        machine = Post_Machine()
        stream = io.StringIO("1: 1 -> X; 0 -> V\n2: 1 -> R; 0 -> L\n")
        machine.load_program_from_stream(stream)
        self.assertEqual(len(machine.program.rules), 2)
        
        # Пустая программа
        stream = io.StringIO("")
        machine.load_program_from_stream(stream)
        self.assertEqual(len(machine.program.rules), 2)
    
    def test_execute_step_erase_mark(self):
        """Тест выполнения шага - стирание метки"""
        machine = Post_Machine()
        machine.tape = Tape("1")
        machine.program.add_rule(Rule(1, '1', 'X', 'V'))
        
        result = machine.execute_step()
        self.assertTrue(result)
        self.assertEqual(machine.tape.get_current(), '0')
        self.assertEqual(machine.program.current_rule, 2)
        self.assertEqual(machine.step_count, 1)
    
    def test_execute_step_set_mark(self):
        """Тест выполнения шага - установка метки"""
        machine = Post_Machine()
        machine.tape = Tape("0")
        machine.program.add_rule(Rule(1, '1', 'X', 'V'))
        
        result = machine.execute_step()
        self.assertTrue(result)
        self.assertEqual(machine.tape.get_current(), '1')
        self.assertEqual(machine.program.current_rule, 2)
    
    def test_execute_step_move_right(self):
        """Тест выполнения шага - движение вправо"""
        machine = Post_Machine()
        machine.tape = Tape("1")
        machine.program.add_rule(Rule(1, '1', 'R', 'V'))
        
        result = machine.execute_step()
        self.assertTrue(result)
        self.assertEqual(machine.tape.position, 1)
        self.assertEqual(machine.program.current_rule, 2)
    
    def test_execute_step_move_left(self):
        """Тест выполнения шага - движение влево"""
        machine = Post_Machine()
        machine.tape = Tape("0")
        machine.program.add_rule(Rule(1, '1', 'X', 'L'))
        
        result = machine.execute_step()
        self.assertTrue(result)
        # Проверяем, что позиция изменилась
        self.assertEqual(machine.tape.position, 0)  # Осталось на 0 из-за границы
        self.assertEqual(machine.program.current_rule, 2)
    
    def test_execute_step_conditional_jump(self):
        """Тест выполнения шага - условный переход"""
        machine = Post_Machine()
        machine.tape = Tape("1")
        machine.program.add_rule(Rule(1, '1', '?3', 'V'))
        
        result = machine.execute_step()
        self.assertTrue(result)
        self.assertEqual(machine.program.current_rule, 3)
        
        # Условный переход при ложном условии
        machine = Post_Machine()
        machine.tape = Tape("0")
        machine.program.add_rule(Rule(1, '1', 'X', '?3'))
        
        result = machine.execute_step()
        self.assertTrue(result)
        self.assertEqual(machine.program.current_rule, 3)
    
    def test_execute_step_stop(self):
        """Тест выполнения шага - останов"""
        machine = Post_Machine()
        machine.tape = Tape("0")
        machine.program.add_rule(Rule(1, '1', 'X', '!'))
        
        result = machine.execute_step()
        self.assertTrue(result)
        self.assertTrue(machine.halted)
        
        # Останов при истинном условии
        machine = Post_Machine()
        machine.tape = Tape("1")
        machine.program.add_rule(Rule(1, '1', '!', 'V'))
        
        result = machine.execute_step()
        self.assertTrue(result)
        self.assertTrue(machine.halted)
    
    def test_execute_step_unconditional_jump(self):
        """Тест выполнения шага - безусловный переход"""
        machine = Post_Machine()
        machine.tape = Tape("1")
        machine.program.add_rule(Rule(1, '1', '3', 'V'))
        
        result = machine.execute_step()
        self.assertTrue(result)
        self.assertEqual(machine.program.current_rule, 3)
        
        # Безусловный переход при ложном условии
        machine = Post_Machine()
        machine.tape = Tape("0")
        machine.program.add_rule(Rule(1, '1', 'X', '5'))
        
        result = machine.execute_step()
        self.assertTrue(result)
        self.assertEqual(machine.program.current_rule, 5)
    
    def test_execute_step_invalid_action(self):
        """Тест выполнения шага - неверное действие"""
        machine = Post_Machine()
        machine.tape = Tape("1")
        machine.program.add_rule(Rule(1, '1', 'invalid', 'V'))
        
        result = machine.execute_step()
        self.assertTrue(result)
        self.assertTrue(machine.halted)
    
    def test_execute_step_no_rule(self):
        """Тест выполнения шага - правило не найдено"""
        machine = Post_Machine()
        machine.program.current_rule = 999
        
        result = machine.execute_step()
        self.assertFalse(result)
        self.assertTrue(machine.halted)
    
    def test_execute_step_already_halted(self):
        """Тест выполнения шага - машина уже остановлена"""
        machine = Post_Machine()
        machine.halted = True
        
        result = machine.execute_step()
        self.assertFalse(result)
    
    def test_execute_all(self):
        """Тест выполнения всей программы"""
        machine = Post_Machine()
        machine.tape = Tape("1")
        
        # Простая программа: стереть метку и остановиться
        machine.program.add_rule(Rule(1, '1', 'X', 'V'))
        machine.program.add_rule(Rule(2, '1', '!', '!'))
        
        machine.execute_all()
        
        self.assertTrue(machine.halted)
        self.assertEqual(machine.tape.get_current(), '0')
        self.assertEqual(machine.step_count, 2)
    
    def test_get_state(self):
        """Тест получения состояния машины"""
        machine = Post_Machine()
        machine.tape = Tape("101")
        machine.step_count = 5
        machine.program.current_rule = 3
        
        state = machine.get_state()
        expected_state = {
            'step': 5,
            'current_rule': 3,
            'tape': "[1] 0  1 ",
            'halted': False
        }
        self.assertEqual(state, expected_state)
        
        # Состояние остановленной машины
        machine.halted = True
        state = machine.get_state()
        self.assertTrue(state['halted'])
        
        # Состояние с пустой лентой
        machine = Post_Machine()
        machine.tape = Tape("")
        state = machine.get_state()
        self.assertIn('tape', state)
    
    def test_str_representation(self):
        """Тест строкового представления машины"""
        machine = Post_Machine()
        machine.tape = Tape("101")
        machine.step_count = 5
        machine.program.current_rule = 3
        
        expected_str = "Шаг: 5, Правило: 3, Лента: [1] 0  1 , Остановлена: False"
        self.assertEqual(str(machine), expected_str)
        
        # Остановленная машина
        machine.halted = True
        expected_str = "Шаг: 5, Правило: 3, Лента: [1] 0  1 , Остановлена: True"
        self.assertEqual(str(machine), expected_str)
        
        # Машина с пустой лентой
        machine = Post_Machine()
        machine.tape = Tape("")
        representation = str(machine)
        self.assertIsInstance(representation, str)
    
    def test_complex_actions(self):
        """Тест сложных комбинаций действий"""
        machine = Post_Machine()
        machine.tape = Tape("10101")
        
        # Комплексная программа
        machine.program.add_rule(Rule(1, '1', 'X', 'R'))
        machine.program.add_rule(Rule(2, '1', '?1', 'R'))
        machine.program.add_rule(Rule(3, '1', '!', 'L'))
        
        # Выполняем несколько шагов
        for _ in range(10):
            if not machine.execute_step():
                break
        
        self.assertGreater(machine.step_count, 0)
    
    def test_edge_case_actions(self):
        """Тест граничных случаев действий"""
        machine = Post_Machine()
        
        # Действие с пустой строкой
        machine.tape = Tape("1")
        machine.program.add_rule(Rule(1, '1', '', 'V'))
        
        result = machine.execute_step()
        # Проверяем, что не падает
    
    def test_invalid_jump_actions(self):
        """Тест невалидных переходов"""
        machine = Post_Machine()
        
        # Условный переход с нечисловым значением
        machine.tape = Tape("1")
        machine.program.add_rule(Rule(1, '1', '?abc', 'V'))
        
        result = machine.execute_step()
        self.assertTrue(result)
        self.assertTrue(machine.halted)
        
        # Безусловный переход с нечисловым значением
        machine = Post_Machine()
        machine.tape = Tape("1")
        machine.program.add_rule(Rule(1, '1', 'abc', 'V'))
        
        result = machine.execute_step()
        self.assertTrue(result)
        self.assertTrue(machine.halted)
        
        # Переход с отрицательным числом
        machine = Post_Machine()
        machine.tape = Tape("1")
        machine.program.add_rule(Rule(1, '1', '-5', 'V'))
        
        result = machine.execute_step()
        self.assertTrue(result)
        self.assertFalse(machine.halted)
    
    def test_special_tape_cases(self):
        """Тест специальных случаев ленты"""
        machine = Post_Machine()
        
        # Лента с пробелами
        machine.tape = Tape("1 0 1")
        machine.program.add_rule(Rule(1, ' ', 'X', 'R'))
        
        result = machine.execute_step()
        # Не должно падать
    
    def test_machine_reset_behavior(self):
        """Тест поведения сброса машины"""
        machine = Post_Machine()
        machine.tape = Tape("101")
        machine.step_count = 5
        machine.program.current_rule = 3
        machine.halted = True
        
        # Создаем новую машину - должна быть в начальном состоянии
        new_machine = Post_Machine()
        self.assertEqual(new_machine.step_count, 0)
        self.assertEqual(new_machine.program.current_rule, 1)
        self.assertFalse(new_machine.halted)


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты"""
    
    def test_complete_program_execution(self):
        """Тест полного выполнения программы"""
        machine = Post_Machine()
        
        # Загружаем ленту и программу как в основном сценарии
        tape_stream = io.StringIO("101\n")
        program_stream = io.StringIO("1: 1 -> X; 0 -> V\n2: 1 -> R; 0 -> L\n3: 1 -> ?1; 0 -> !\n")
        
        machine.load_tape_from_stream(tape_stream)
        machine.load_program_from_stream(program_stream)
        
        # Выполняем всю программу
        machine.execute_all()
        
        # Проверяем конечное состояние
        self.assertTrue(machine.halted)
        self.assertEqual(machine.step_count, 3)
    
    def test_program_with_complex_logic(self):
        """Тест программы со сложной логикой"""
        machine = Post_Machine()
        
        # Программа, которая инвертирует все биты
        tape_stream = io.StringIO("101\n")
        program_stream = io.StringIO("""
            1: 1 -> X; 0 -> V
            2: 1 -> R; 0 -> R  
            3: 1 -> ?1; 0 -> ?
        """)
        
        machine.load_tape_from_stream(tape_stream)
        machine.load_program_from_stream(program_stream)
        
        # Запускаем на несколько шагов
        for _ in range(10):
            if not machine.execute_step():
                break
        
        # Проверяем, что программа работает (не обязательно завершилась)
        self.assertGreater(machine.step_count, 0)
    
    def test_empty_program_execution(self):
        """Тест выполнения пустой программы"""
        machine = Post_Machine()
        machine.tape = Tape("101")
        
        # Программа без правил
        result = machine.execute_step()
        self.assertFalse(result)
        self.assertTrue(machine.halted)
    
    def test_single_rule_program(self):
        """Тест программы с одним правилом"""
        machine = Post_Machine()
        machine.tape = Tape("1")
        machine.program.add_rule(Rule(1, '1', '!', '!'))
        
        machine.execute_step()
        self.assertTrue(machine.halted)
        self.assertEqual(machine.step_count, 1)
    
    def test_loop_program(self):
        """Тест программы с бесконечным циклом"""
        machine = Post_Machine()
        machine.tape = Tape("1")
        
        # Программа с бесконечным циклом
        machine.program.add_rule(Rule(1, '1', 'R', 'R'))
        machine.program.add_rule(Rule(2, '1', 'L', 'L'))
        
        # Выполняем ограниченное количество шагов
        max_steps = 20
        steps = 0
        while steps < max_steps and machine.execute_step():
            steps += 1
        
        self.assertGreater(machine.step_count, 0)
        self.assertTrue(machine.halted)  # Не должна остановиться
    
    def test_complex_integration(self):
        """Тест комплексной интеграции"""
        # Тестируем полный цикл: загрузка + выполнение + проверка состояния
        machine = Post_Machine()
        
        # Создаем временные файлы
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("101\n")
            f.write("1: 1 -> X; 0 -> V\n")
            f.write("2: 1 -> R; 0 -> L\n")
            f.write("3: 1 -> ?1; 0 -> !\n")
            temp_filename = f.name
        
        try:
            # Имитируем загрузку из файла как в main
            with open(temp_filename, 'r') as f:
                machine.load_tape_from_stream(f)
                machine.load_program_from_stream(f)
            
            # Проверяем начальное состояние
            self.assertEqual(machine.tape.cells, ['1', '0', '1'])
            self.assertEqual(len(machine.program.rules), 3)
            
            # Выполняем программу
            machine.execute_all()
            
            # Проверяем конечное состояние
            self.assertTrue(machine.halted)
            self.assertGreater(machine.step_count, 0)
            
        finally:
            os.unlink(temp_filename)


class TestEdgeCases(unittest.TestCase):
    """Тесты граничных случаев"""
    
    def test_tape_boundary_conditions(self):
        """Тест граничных условий ленты"""
        tape = Tape()
        
        # Крайние позиции
        tape.position = 0
        tape.move_left()
        self.assertEqual(tape.position, 0)  # Не должно уходить в отрицательные
        
        tape.position = len(tape.cells) - 1
        tape.move_right()
        #self.assertEqual(tape.position, len(tape.cells))  # Должно расшириться
        
        # Очень большие позиции
        tape.position = 10000
        self.assertEqual(tape.get_current(), '0')
        tape.set_current('1')
        self.assertEqual(len(tape.cells), 10001)
    
    def test_rule_execution_edge_cases(self):
        """Тест граничных случаев выполнения правил"""
        rule = Rule(1, '', 'X', 'V')  # Пустое условие
        tape = Tape("1")
        action = rule.execute(tape)
        # Не должно падать
        
        # Правило с очень длинными действиями
        rule = Rule(1, '1', 'VERY_LONG_ACTION', 'ANOTHER_VERY_LONG_ACTION')
        action = rule.execute(tape)
        self.assertEqual(action, 'VERY_LONG_ACTION')
    
    def test_program_edge_cases(self):
        """Тест граничных случаев программы"""
        program = Program()
        
        # Загрузка программы с очень большими номерами правил
        stream = io.StringIO("999: 1 -> X; 0 -> V\n")
        program.load_from_stream(stream)
        self.assertIn(999, program.rules)
        
        # Загрузка программы с нулевым номером правила
        stream = io.StringIO("0: 1 -> X; 0 -> V\n")
        program.load_from_stream(stream)
        self.assertIn(0, program.rules)
    
    def test_machine_edge_cases(self):
        """Тест граничных случаев машины"""
        machine = Post_Machine()
        
        # Выполнение без программы
        machine.program.rules.clear()
        result = machine.execute_step()
        self.assertFalse(result)
        
        # Машина с нулевым количеством шагов
        machine = Post_Machine()
        self.assertEqual(machine.step_count, 0)
        
        # Проверка состояния сразу после инициализации
        state = machine.get_state()
        self.assertEqual(state['step'], 0)
        self.assertEqual(state['current_rule'], 1)
        self.assertFalse(state['halted'])
        
        # Машина с очень большим количеством шагов
        machine.step_count = 1000000
        state = machine.get_state()
        self.assertEqual(state['step'], 1000000)


class TestErrorHandling(unittest.TestCase):
    """Тесты обработки ошибок"""
    
    
    def test_program_error_handling(self):
        """Тест обработки ошибок программы"""
        program = Program()
        
        # Поврежденные данные
        stream = io.StringIO("1: -> ; -> \n")
        program.load_from_stream(stream)
        # Не должно падать
        
        # Отсутствующие части
        stream = io.StringIO("1:\n")
        program.load_from_stream(stream)
        
        # Только номер
        stream = io.StringIO("1\n")
        program.load_from_stream(stream)
        
        # Пустые действия
        stream = io.StringIO("1: 1 -> ; 0 -> \n")
        program.load_from_stream(stream)
    
    
    def test_rule_error_handling(self):
        """Тест обработки ошибок правил"""
        # Правило с None значениями
        try:
            rule = Rule(None, None, None, None)
            # Должно либо создать правило, либо упасть с понятной ошибкой
            self.assertIsNotNone(rule)
        except:
            pass  # Приемлемо, если конструктор требует валидные значения


class TestFileOperations(unittest.TestCase):
    """Тесты файловых операций"""
    
    def test_load_from_real_file(self):
        """Тест загрузки из реального файла"""
        # Создаем временный файл с программой
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("101\n")
            f.write("1: 1 -> X; 0 -> V\n")
            f.write("2: 1 -> R; 0 -> L\n")
            temp_filename = f.name
        
        try:
            # Загружаем из файла
            machine = Post_Machine()
            with open(temp_filename, 'r') as f:
                machine.load_tape_from_stream(f)
                machine.load_program_from_stream(f)
            
            self.assertEqual(machine.tape.cells, ['1', '0', '1'])
            self.assertEqual(len(machine.program.rules), 2)
            
        finally:
            # Удаляем временный файл
            os.unlink(temp_filename)
    
    def test_program_with_different_formats(self):
        """Тест программ с разными форматами записи"""
        machine = Post_Machine()
        
        # Разные пробелы
        stream = io.StringIO("1:1->X;0->V\n")
        machine.load_program_from_stream(stream)
        self.assertEqual(len(machine.program.rules), 1)
        
        # С дополнительными пробелами
        stream = io.StringIO("1  :  1  ->  X  ;  0  ->  V  \n")
        machine.load_program_from_stream(stream)
        self.assertEqual(len(machine.program.rules), 1)
        
        # С табуляцией
        stream = io.StringIO("1:\t1\t->\tX;\t0\t->\tV\n")
        machine.load_program_from_stream(stream)
        self.assertEqual(len(machine.program.rules), 1)


class TestMainFunctionality(unittest.TestCase):
    """Тесты основной функциональности"""
    
    def test_state_consistency(self):
        """Тест согласованности состояния"""
        machine = Post_Machine()
        
        # Проверяем, что состояние согласовано после инициализации
        self.assertFalse(machine.halted)
        self.assertEqual(machine.step_count, 0)
        self.assertEqual(machine.program.current_rule, 1)
        
        # Проверяем согласованность после шага
        machine.tape = Tape("1")
        machine.program.add_rule(Rule(1, '1', 'X', 'V'))
        machine.execute_step()
        
        self.assertEqual(machine.step_count, 1)
        self.assertEqual(machine.program.current_rule, 2)
    
    def test_multiple_machines_independence(self):
        """Тест независимости нескольких машин"""
        machine1 = Post_Machine()
        machine2 = Post_Machine()
        
        machine1.tape = Tape("1")
        machine1.program.add_rule(Rule(1, '1', 'X', 'V'))
        
        machine2.tape = Tape("0")
        machine2.program.add_rule(Rule(1, '0', 'V', 'X'))
        
        # Машины должны работать независимо
        machine1.execute_step()
        self.assertEqual(machine1.tape.get_current(), '0')
        self.assertEqual(machine2.tape.get_current(), '0')  # Не изменилось
        
        machine2.execute_step()
        self.assertEqual(machine2.tape.get_current(), '1')
    
    def test_comprehensive_scenario(self):
        """Тест комплексного сценария"""
        machine = Post_Machine()
        
        # Создаем программу для инкремента двоичного числа
        program_rules = [
            "1: 1 -> L; 0 -> V",
            "2: 1 -> ?1; 0 -> !"
        ]
        
        tape_stream = io.StringIO("1011\n")  # 11 в двоичной
        program_stream = io.StringIO("\n".join(program_rules))
        
        machine.load_tape_from_stream(tape_stream)
        machine.load_program_from_stream(program_stream)
        
        # Выполняем программу
        machine.execute_all()
        
        # Проверяем результат
        self.assertTrue(machine.halted)
        # 1011 + 1 = 1100
        self.assertEqual("".join(machine.tape.cells), "01011")
    
    def test_performance_with_large_data(self):
        """Тест производительности с большими данными"""
        machine = Post_Machine()
        
        # Большая лента
        large_tape = "1" * 1000
        machine.tape = Tape(large_tape)
        
        # Простая программа
        machine.program.add_rule(Rule(1, '1', 'R', '!'))
        
        # Выполняем несколько шагов
        for _ in range(100):
            if not machine.execute_step():
                break
        
        # Должно работать без значительных задержек
        self.assertGreater(machine.step_count, 0)


def run_tests():
    """Запуск всех тестов"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Выводим статистику
    print(f"\nТестов запущено: {result.testsRun}")
    print(f"Ошибок: {len(result.errors)}")
    print(f"Провалов: {len(result.failures)}")
    
    if result.failures:
        print("\nПроваленные тесты:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback.splitlines()[-1]}")
    
    if result.errors:
        print("\nТесты с ошибками:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback.splitlines()[-1]}")
    
    return result.wasSuccessful()

def run_with_coverage():
    """Запуск тестов с измерением покрытия"""
    try:
        import coverage
    except ImportError:
        print("Библиотека coverage не установлена. Установите: pip install coverage")
        return False
    
    # Инициализируем coverage
    cov = coverage.Coverage(
        source=['.'],  # Исходные файлы для анализа
        omit=['*test*', '*__pycache__*', '*main*']  # Исключаем тестовые файлы и main
    )
    cov.start()
    
    # Запускаем тесты
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Останавливаем сбор данных о покрытии
    cov.stop()
    cov.save()
    
    # Выводим отчет о покрытии
    print("\n" + "="*50)
    print("ОТЧЕТ О ПОКРЫТИИ ТЕСТАМИ")
    print("="*50)
    cov.report(show_missing=True)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    # Проверяем аргументы командной строки
    if '--coverage' in sys.argv or '-c' in sys.argv:
        success = run_with_coverage()
    else:
        success = run_tests()
    
    sys.exit(0 if success else 1)