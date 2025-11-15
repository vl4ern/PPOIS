# machine_test.py
import sys
import os

# ===============================================================
# ЗАПУСК coverage ДО импортов, чтобы считались верхние строки
# ===============================================================
try:
    import coverage
    cov = coverage.Coverage(source=['.'], omit=['*test*', '*__pycache__*'])
    cov.start()
except ImportError:
    cov = None

# ===============================================================
# Импорты после запуска coverage
# ===============================================================
import unittest
import io
import tempfile
from unittest import mock
import importlib

sys.path.append(os.path.dirname(__file__))

# Импортируем тестируемые модули
machine_tape = importlib.import_module("machine_tape")
machine_rule = importlib.import_module("machine_rule")
machine_program = importlib.import_module("machine_program")
machine_post = importlib.import_module("machine_post")
machine_main = importlib.import_module("machine_main")

Tape = machine_tape.Tape
Rule = machine_rule.Rule
Program = machine_program.Program
Post_Machine = machine_post.Post_Machine


# ===============================================================
# =============== ТЕСТЫ (твоя логика сохранена) =================
# ===============================================================

# ----------------------------
# Tests for machine_tape.py
# ----------------------------
class TapeFullCoverageTests(unittest.TestCase):
    def test_init_defaults_and_with_data(self):
        t = Tape()
        self.assertEqual(t.cells, ['0'])
        self.assertEqual(t.position, 0)
        t2 = Tape("")
        self.assertEqual(t2.cells, ['0'])
        t3 = Tape("101")
        self.assertEqual(t3.cells, ['1', '0', '1'])

    def test_get_current_in_bounds_and_out(self):
        t = Tape("101")
        self.assertEqual(t.get_current(), '1')
        t.position = 1
        self.assertEqual(t.get_current(), '0')
        t.position = 100
        self.assertEqual(t.get_current(), '0')
        t.position = -5
        self.assertEqual(t.get_current(), '0')

    def test_set_current_in_bounds(self):
        t = Tape("101")
        t.position = 1
        t.set_current('X')
        self.assertEqual(t.cells[1], 'X')

    def test_set_current_expand_right(self):
        t = Tape("1")
        t.position = 5
        t.set_current('9')
        self.assertEqual(t.cells[5], '9')
        self.assertEqual(len(t.cells), 6)

    def test_set_current_expand_left(self):
        t = Tape("1")
        t.position = -2
        t.set_current('A')
        self.assertGreaterEqual(t.position, 0)
        self.assertEqual(t.cells[0], 'A')

    def test_move_left_insert_and_move_right_append(self):
        t = Tape("101")
        t.position = 0
        t.move_left()
        self.assertEqual(t.position, 0)
        self.assertGreaterEqual(len(t.cells), 4)
        t = Tape("1")
        t.position = 0
        t.move_right()
        self.assertEqual(t.position, 1)
        self.assertEqual(t.cells[1], '0')

    def test_load_from_stream_various_inputs(self):
        t = Tape()
        t.load_from_stream(io.StringIO("\n"))
        self.assertEqual(t.cells, ['0'])

        # Строка с пробелами — должны сохраниться все символы, включая пробелы
        t.load_from_stream(io.StringIO(" 1 0 \n"))
# .strip() убирает пробелы по краям, значит должно быть ['1',' ','0']
        self.assertEqual(t.cells, list("1 0"))

        # Обычная строка без пробелов
        t.load_from_stream(io.StringIO("1110\n"))
        self.assertEqual(t.cells, list("1110"))


    def test_str_representation_various(self):
        t = Tape("101")
        t.position = 0
        s0 = str(t)
        self.assertIn('[1]', s0)
        t.position = 1
        s1 = str(t)
        self.assertIn('[0]', s1)
        t_empty = Tape()
        self.assertEqual(str(t_empty), "[0]")

    def test_long_and_edge_positions(self):
        long_s = "1" * 200
        t = Tape(long_s)
        self.assertEqual(len(t.cells), 200)
        t.position = 1000
        self.assertEqual(t.get_current(), '0')
        t.set_current('7')
        self.assertEqual(len(t.cells), 1001)
        self.assertEqual(t.cells[-1], '7')


# ----------------------------
# Tests for machine_rule.py
# ----------------------------
class RuleFullCoverageTests(unittest.TestCase):
    def test_execute_true_false(self):
        r = Rule(1, '1', 'X', 'V')
        t = Tape("1")
        self.assertEqual(r.execute(t), 'X')
        t = Tape("0")
        self.assertEqual(r.execute(t), 'V')

    def test_execute_with_space_and_empty_condition(self):
        r_space = Rule(2, ' ', 'A', 'B')
        t = Tape(" 1")
        t.position = 0
        self.assertEqual(r_space.execute(t), 'A')
        r_empty = Rule(3, '', 'A2', 'B2')
        t = Tape("1")
        self.assertEqual(r_empty.execute(t), 'B2')

    def test_str_various_forms(self):
        r = Rule(4, '0', '?5', '!')
        s = str(r)
        self.assertIn("4:", s)
        self.assertIn("-> ?5", s)
        self.assertIn("-> !", s)

    def test_rule_with_none_values_behaviour(self):
        r = Rule(None, None, None, None)
        s = str(r)
        self.assertIsInstance(s, str)
        t = Tape("1")
        self.assertIsNone(r.execute(t))


# ----------------------------
# Tests for machine_program.py
# ----------------------------
class ProgramFullCoverageTests(unittest.TestCase):
    def test_add_get_remove_and_str(self):
        p = Program()
        r1 = Rule(1, '1', 'X', 'V')
        p.add_rule(r1)
        self.assertIs(p.get_rule(1), r1)
        p.remove_rule(1)
        self.assertIsNone(p.get_rule(1))
        self.assertEqual(p.view_rules(), "")
        self.assertEqual(str(p), "")

    def test_view_rules_sorted_order(self):
        p = Program()
        p.add_rule(Rule(5, '0', 'R', 'L'))
        p.add_rule(Rule(1, '1', 'X', 'V'))
        v = p.view_rules()
        lines = v.splitlines()
        self.assertTrue(lines[0].startswith("1:"))
        self.assertTrue(any(line.startswith("5:") for line in lines))

    def test_load_from_stream_good_lines(self):
        p = Program()
        s = io.StringIO("1: 1 -> X; 0 -> V\n2: 0 -> R; 1 -> L\n")
        p.load_from_stream(s)
        self.assertIn(1, p.rules)
        self.assertIn(2, p.rules)
        self.assertEqual(p.get_rule(1).action_true, 'X')

    def test_load_from_stream_malformed_lines_and_errors_printed(self):
        p = Program()
        bads = [
            "no_colon_here\n",
            "abc: broken -> X; 0 -> V\n",
            "2: missing_arrow X; 0 V\n",
            "3: 1 -> X;   \n",
            "4: 1->X;0->V\n"
        ]
        with mock.patch('builtins.print') as mp:
            for line in bads:
                p.load_from_stream(io.StringIO(line))
            self.assertTrue(mp.call_count >= 1)
        if 4 in p.rules:
            self.assertEqual(p.rules[4].condition, '1')

    def test_load_from_stream_comments_and_blank(self):
        p = Program()
        s = io.StringIO("# comment\n\n1: 1 -> X; 0 -> V\n# another\n")
        p.load_from_stream(s)
        self.assertIn(1, p.rules)

    def test_add_duplicate_rule_replaces(self):
        p = Program()
        p.add_rule(Rule(1, '1', 'A', 'B'))
        p.add_rule(Rule(1, '0', 'C', 'D'))
        self.assertEqual(p.get_rule(1).condition, '0')


# ----------------------------
# Tests for machine_post.py
# ----------------------------
class PostMachineFullCoverageTests(unittest.TestCase):
    def test_init_state_and_loading(self):
        m = Post_Machine()
        self.assertFalse(m.halted)
        s = io.StringIO("101\n")
        m.load_tape_from_stream(s)
        s2 = io.StringIO("1: 1 -> X; 0 -> V\n")
        m.load_program_from_stream(s2)
        self.assertIn(1, m.program.rules)

    def test_execute_steps_basic_actions(self):
        m = Post_Machine()
        m.tape = Tape("0")
        m.program.add_rule(Rule(1, '0', 'V', '!'))
        m.program.current_rule = 1
        self.assertTrue(m.execute_step())
        self.assertEqual(m.tape.get_current(), '1')

    def test_execute_conditional_true_and_false(self):
        m = Post_Machine()
        m.tape = Tape("1")
        m.program.add_rule(Rule(1, '1', '?3', 'V'))
        m.program.add_rule(Rule(3, '1', '!', '!'))
        m.program.current_rule = 1
        self.assertTrue(m.execute_step())
        self.assertEqual(m.program.current_rule, 3)

    def test_execute_unconditional_numeric_and_invalid(self):
        m = Post_Machine()
        m.tape = Tape("0")
        m.program.add_rule(Rule(1, '1', '5', '10'))
        m.program.current_rule = 1
        self.assertTrue(m.execute_step())

    def test_execute_halt_action_and_execute_all(self):
        m = Post_Machine()
        m.tape = Tape("1")
        m.program.add_rule(Rule(1, '1', 'X', 'V'))
        m.program.add_rule(Rule(2, '1', '!', '!'))
        m.program.current_rule = 1
        m.execute_all()
        self.assertTrue(m.halted)

    def test_execute_step_when_no_rule_or_already_halted(self):
        m = Post_Machine()
        m.program.current_rule = 999
        self.assertFalse(m.execute_step())
        self.assertTrue(m.halted)
        m = Post_Machine()
        m.halted = True
        self.assertFalse(m.execute_step())

    def test_get_state_and_str_contains_expected_fields(self):
        m = Post_Machine()
        m.tape = Tape("101")
        m.step_count = 4
        s = str(m)
        self.assertIn("Шаг:", s)
        st = m.get_state()
        self.assertIn("tape", st)


# ----------------------------
# Tests for machine_main.py
# ----------------------------
class MainModuleCoverageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
        self.tmp.write("101\n")
        self.tmp.write("1: 1 -> X; 0 -> V\n")
        self.tmp.write("2: 1 -> !; 0 -> R\n")
        self.tmp.close()

    def tearDown(self):
        try:
            os.unlink(self.tmp.name)
        except Exception:
            pass

    @mock.patch('builtins.print')
    def test_main_no_args_causes_exit(self, mock_print):
        import PPOIS.First_lab.Post_Machine.main as mm
        old_argv = sys.argv[:]
        sys.argv = ['machine_main.py']
        with self.assertRaises(SystemExit):
            mm.main()
        mock_print.assert_called_with("Использование: python post_machine.py <файл> [-log]")
        sys.argv = old_argv

    @mock.patch('builtins.print')
    def test_main_normal_and_log_modes_and_file_not_found_and_exceptions(self, mock_print):
        import PPOIS.First_lab.Post_Machine.main as mm
        old_argv = sys.argv[:]
        sys.argv = ['machine_main.py', self.tmp.name]
        mm.main()
        mock_print.assert_any_call("Начальное состояние:")
        mock_print.assert_any_call("\nФинальное состояние:")
        sys.argv = ['machine_main.py', self.tmp.name, '-log']
        mm.main()
        self.assertTrue(any("После шага" in " ".join(map(str, c)) for c in mock_print.call_args_list))
        sys.argv = ['machine_main.py', "no_such_file_12345.txt"]
        mm.main()
        mock_print.assert_called_with("Файл no_such_file_12345.txt не найден")
        with mock.patch('machine_main.Post_Machine', side_effect=RuntimeError("boom")):
            sys.argv = ['machine_main.py', self.tmp.name]
            mm.main()
            mock_print.assert_called_with("Ошибка: boom")
        sys.argv = old_argv


# ----------------------------
# Extra Edge Tests
# ----------------------------
class ExtraEdgeCoverageTests(unittest.TestCase):
    def test_program_load_only_number_line(self):
        p = Program()
        with mock.patch('builtins.print'):
            p.load_from_stream(io.StringIO("1:\n"))
        self.assertIsInstance(p.rules, dict)

    def test_program_load_compact_no_spaces(self):
        p = Program()
        p.load_from_stream(io.StringIO("1:1->X;0->V\n"))
        self.assertIn(1, p.rules)

    def test_post_machine_negative_jump(self):
        m = Post_Machine()
        m.tape = Tape('1')
        m.program.add_rule(Rule(1, '1', '-5', 'V'))
        m.program.current_rule = 1
        m.execute_step()
        self.assertEqual(m.program.current_rule, -5)

    def test_post_machine_action_empty_string(self):
        m = Post_Machine()
        m.tape = Tape('1')
        m.program.add_rule(Rule(1, '1', '', 'V'))
        m.program.current_rule = 1
        m.execute_step()
        self.assertTrue(m.halted)


# ===============================================================
# Финальный запуск coverage + тестов
# ===============================================================
if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if cov:
        cov.stop()
        cov.save()
        print("\n=== COVERAGE REPORT ===")
        cov.report(show_missing=True)

    sys.exit(0 if result.wasSuccessful() else 1)
