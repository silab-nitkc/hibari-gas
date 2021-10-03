import unittest
import z3
import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from code_generator import * #nopep

class TestInstructionSequenceGenerator(unittest.TestCase):
    def test_generate_add(self):
        const = []
        inst_seq = InstructionSequence()
        inst_seq.add_instruction(Instruction(all))

        tl1 = Timeline(2)
        const += tl1.get_state(0).set_values([1, 2, 3, 4])
        const += tl1.get_state(1).set_values([1, 2, 7, 4])
        const += tl1.get_const()
        const += inst_seq.instructions[0].get_const(
            tl1.get_state(0), tl1.get_state(1))

        tl2 = Timeline(2)
        const += tl2.get_state(0).set_values([101, 102, 103, 104])
        const += tl2.get_state(1).set_values([101, 102, 207, 104])
        const += tl2.get_const()
        const += inst_seq.instructions[0].get_const(
            tl2.get_state(0), tl2.get_state(1))

        const += get_pc_const(inst_seq.instructions[0])

        sl = z3.Solver()
        sl.add(const)
        sl.check()
        m = sl.model()

        expected = {
            "instruction_id": 0,
            "instruction": "Add",
            "dst": 2,
            "src": 3,
            "src_is_immediate": 0,
            "immediate": None
        }
        result = inst_seq.instructions[0].eval(m)
        self.assertEqual(expected, result)

    def test_generate_add_with_negative_values(self):
        const = []
        inst_seq = InstructionSequence()
        inst_seq.add_instruction(Instruction(all))

        tl1 = Timeline(2)
        const += tl1.get_state(0).set_values([12, 34, 56, -78])
        const += tl1.get_state(1).set_values([12, 34, -22, -78])
        const += tl1.get_const()
        const += inst_seq.instructions[0].get_const(
            tl1.get_state(0), tl1.get_state(1))

        tl2 = Timeline(2)
        const += tl2.get_state(0).set_values([1, 2, -3, 4])
        const += tl2.get_state(1).set_values([1, 2, 1, 4])
        const += tl2.get_const()
        const += inst_seq.instructions[0].get_const(
            tl2.get_state(0), tl2.get_state(1))

        const += get_pc_const(inst_seq.instructions[0])

        sl = z3.Solver()
        sl.add(const)
        sl.check()
        m = sl.model()

        expected = {
            "instruction_id": 0,
            "instruction": "Add",
            "dst": 2,
            "src": 3,
            "src_is_immediate": 0,
            "immediate": None
        }
        result = inst_seq.instructions[0].eval(m)
        self.assertEqual(expected, result)

    def test_generate_sub(self):
        const = []
        inst_seq = InstructionSequence()
        inst_seq.add_instruction(Instruction(all))

        tl1 = Timeline(2)
        const += tl1.get_state(0).set_values([12, 34, 56, 78])
        const += tl1.get_state(1).set_values([12, 34, 56, 22])
        const += tl1.get_const()
        const += inst_seq.instructions[0].get_const(
            tl1.get_state(0), tl1.get_state(1))

        tl2 = Timeline(2)
        const += tl2.get_state(0).set_values([1, 2, 3, 4])
        const += tl2.get_state(1).set_values([1, 2, 3, 1])
        const += tl2.get_const()
        const += inst_seq.instructions[0].get_const(
            tl2.get_state(0), tl2.get_state(1))

        const += get_pc_const(inst_seq.instructions[0])

        sl = z3.Solver()
        sl.add(const)
        sl.check()
        m = sl.model()

        expected = {
            "instruction_id": 1,
            "instruction": "Sub",
            "dst": 3,
            "src": 2,
            "src_is_immediate": 0,
            "immediate": None
        }
        result = inst_seq.instructions[0].eval(m)
        self.assertEqual(expected, result)

    def test_generate_sub_with_negative_values(self):
        const = []
        inst_seq = InstructionSequence()
        inst_seq.add_instruction(Instruction(all))

        tl1 = Timeline(2)
        const += tl1.get_state(0).set_values([12, 34, 56, 78])
        const += tl1.get_state(1).set_values([12, 34, -22, 78])
        const += tl1.get_const()
        const += inst_seq.instructions[0].get_const(
            tl1.get_state(0), tl1.get_state(1))

        tl2 = Timeline(2)
        const += tl2.get_state(0).set_values([1, 2, -3, 4])
        const += tl2.get_state(1).set_values([1, 2, -7, 4])
        const += tl2.get_const()
        const += inst_seq.instructions[0].get_const(
            tl2.get_state(0), tl2.get_state(1))

        const += get_pc_const(inst_seq.instructions[0])

        sl = z3.Solver()
        sl.add(const)
        sl.check()
        m = sl.model()

        expected = {
            "instruction_id": 1,
            "instruction": "Sub",
            "dst": 2,
            "src": 3,
            "src_is_immediate": 0,
            "immediate": None
        }
        result = inst_seq.instructions[0].eval(m)
        self.assertEqual(expected, result)

if __name__ == "__main__":
    unittest.main()
