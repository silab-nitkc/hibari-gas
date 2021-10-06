import unittest
import z3
import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from gas_obfuscator import *  # noqa


class TestLine(unittest.TestCase):
    def test_convert_to_line(self):
        target = {
            "instruction_id": 0,
            "instruction": "add",
            "dst": 2,
            "src": 3,
            "src_is_immediate": 0,
            "immediate": None
        }
        operands: list[str] = [f"reg{i}" for i in range(4)]

        result: Line = Line._convert_to_line(target, operands)
        print(result.__dict__)

    def test_convert_to_lines(self):
        target: list[dict] = [
            {
                "instruction_id": 0,
                "instruction": "add",
                "dst": 2,
                "src": 3,
                "src_is_immediate": 0,
                "immediate": None
            },
            {
                "instruction_id": 1,
                "instruction": "sub",
                "dst": 2,
                "src": None,
                "src_is_immediate": 1,
                "immediate": 123
            }
        ]
        operands: list[str] = [f"reg{i}" for i in range(4)]

        result: list[Line] = Line.convert_to_lines(target, operands)
        print([i.__dict__ for i in result])


if __name__ == "__main__":
    unittest.main()
