from lark import Transformer, Lark
from .line import Line
import os
import sys

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


class Parser(Transformer):
    dummies = []

    def __init__(self, line: Line):
        super().__init__()
        self.line: Line = line

    def exp(self, tree):
        pass

    def define_dummy(self, tree):
        Parser.dummies += [tree[0]["name"]]
        self.line.label = tree[0]["name"]

    def label(self, tree):
        self.line.label = tree[0]["name"]

    def add(self, tree):
        self.line.set_op(sys._getframe().f_code.co_name, tree)

    def sub(self, tree):
        self.line.set_op(sys._getframe().f_code.co_name, tree)

    def xor(self, tree):
        self.line.set_op(sys._getframe().f_code.co_name, tree)

    def and_(self, tree):
        self.line.set_op("and", tree)

    def or_(self, tree):
        self.line.set_op("or", tree)

    def mov(self, tree):
        self.line.set_op(sys._getframe().f_code.co_name, tree)

    def jz(self, tree):
        self.line.set_op(sys._getframe().f_code.co_name, tree)

    def jnz(self, tree):
        self.line.set_op(sys._getframe().f_code.co_name, tree)

    def suffix(self, tree) -> str:
        return str(tree[0])

    def operand(self, tree) -> dict:
        return tree[0]

    def x64register(self, tree) -> dict:
        return {
            "name": str(tree[0]),
            "has_memory_ref": False,
            "is_immediate": False,
        }

    def x32register(self, tree) -> dict:
        return {
            "name": str(tree[0]),
            "has_memory_ref": False,
            "is_immediate": False,
        }

    def name(self, tree) -> dict:
        return {
            "name": str(tree[0]),
            "has_memory_ref": True,
            "is_immediate": False,
        }

    def dummy(self, tree) -> dict:
        return {
            "name": str(tree[0]),
            "has_memory_ref": True,
            "is_immediate": False,
        }

    def immidiate(self, tree) -> dict:
        return {
            "name": None,
            "has_memory_ref": False,
            "is_immediate": True,
            "immediate": int(tree[0])
        }
