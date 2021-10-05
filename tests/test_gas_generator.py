import unittest
import z3
import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from gas_obfuscator import *  # noqa


class TestInstructionSequenceGenerator(unittest.TestCase):
    def test_generate_add(self):

        target = {
            "instruction_id": 0,
            "instruction": "add",
            "dst": 2,
            "src": 3,
            "src_is_immediate": 0,
            "immediate": None
        }

        generator: GASGenerator = GASGenerator(
            ["reg0", "reg1", "reg2", "reg3"], "q")
        res: str = generator.generate_code(target)
        expected = "addq reg3, reg2"
        self.assertEqual(res, expected)

    def test_generate_add_immediate(self):
        target = {
            "instruction_id": 0,
            "instruction": "add",
            "dst": 2,
            "src": None,
            "src_is_immediate": 1,
            "immediate": 12
        }

        generator: GASGenerator = GASGenerator(
            ["reg0", "reg1", "reg2", "reg3"], "q")
        res: str = generator.generate_code(target)
        expected = "addq $12, reg2"
        self.assertEqual(res, expected)

    def test_generate_GAS(self):
        target = [{
            "instruction_id": 0,
            "instruction": "mov",
            "dst": 1,
            "src": 0,
            "src_is_immediate": 0,
            "immediate": None
        }, {
            "instruction_id": 0,
            "instruction": "add",
            "dst": 1,
            "src": None,
            "src_is_immediate": 1,
            "immediate": 12
        }]

        generator: GASGenerator = GASGenerator(["reg0", "reg1"], "q")
        res: list[str] = generator.generate_GAS(target)
        expected: list[str] = ["movq reg0, reg1", "addq $12, reg1"]
        self.assertEqual(res, expected)


if __name__ == "__main__":
    unittest.main()
