import unittest
import sys
import os
from lark import Lark
import os
import sys

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from gas_obfuscator import *  # noqa

with open(os.path.dirname(__file__) + '/../gas_obfuscator/gas.lark', encoding="utf-8") as g:
    lark_parser = Lark(g.read(), start="exp")


def parse(raw):
    try:
        res: Line = Line(raw)
        tree = lark_parser.parse(raw)
        Parser(res).transform(tree)
        return res
    except:
        return Line(raw)


class TestGASParser(unittest.TestCase):
    def test_parse_add(self):
        target: str = r"addq $12, %rax"

        res: Line = parse(target)
        expected: dict = {
            "raw": target,
            "op": "add",
            "dst": r"%rax",
            "dst_has_memory_ref": False,
            "src": "12",
            "src_has_memory_ref": False,
            "src_is_immediate": True,
            "immediate": 12,
            "label": None,
            "suffix": "q"
        }
        self.assertEqual(res.__dict__, expected)

    def test_parse_label(self):
        target: str = r"label123:"

        res: Line = parse(target)
        expected: dict = {
            "raw": target,
            "op": None,
            "dst": None,
            "dst_has_memory_ref": None,
            "src": None,
            "src_has_memory_ref": None,
            "src_is_immediate": None,
            "immediate": None,
            "label": "label123",
            "suffix": None,
        }
        self.assertEqual(res.__dict__, expected)

    def test_parse_define_label(self):
        target: str = r"R12345:  .space 160"

        res: Line = parse(target)
        expected: dict = {
            "raw": target,
            "op": None,
            "dst": None,
            "dst_has_memory_ref": None,
            "src": None,
            "src_has_memory_ref": None,
            "src_is_immediate": None,
            "immediate": None,
            "label": "R12345",
            "suffix": None,
        }
        self.assertEqual(res.__dict__, expected)

    def test_list_operands(self):
        target: list[str] = """
            dummy: .space 160

            addq $12, %rax
            subq $12, %rax
            movq $12, %rax
        """.split("\n")

        temp: list[Line] = list(map(parse, target))
        res: dict = Line.get_operands(temp)

        expected: dict = {
            "dummy": None,
            r"%rax": None,
        }
        self.assertEqual(res, expected)


if __name__ == "__main__":
    unittest.main()
