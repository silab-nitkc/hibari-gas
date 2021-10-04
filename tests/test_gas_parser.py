import unittest
import sys
import os
from lark import Lark
import os, sys

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from gas_obfuscator import *  # nopep

with open(os.path.dirname(__file__) + '/../gas_obfuscator/gas.lark', encoding="utf-8") as g:
    lark_parser = Lark(g.read(), start="exp")

def parse(raw):
    try:
        res: Line = Line(raw)
        tree = lark_parser.parse(raw)
        Parser(res).transform(tree)
        return res
    except:
        return Line('')

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

if __name__ == "__main__":
    unittest.main()
