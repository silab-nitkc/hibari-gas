from .operand import Operand, OperandDict
from .parser import Parser
from lark import Lark
from os.path import dirname

with open(dirname(__file__) + '/gas.lark', encoding="utf-8") as g:
    lark_parser = Lark(g.read(), start="exp")

class Line:
    def __init__(self, raw: str) -> None:
        self.raw = raw
        self.tree = None
        self.op = None
        self.operands = []
        self.suffix = None
        self.bits = 64
        self.label = None

        self.parse()
    
    def parse(self):
        try:
            self.tree = lark_parser.parse(self.raw)
            Parser(self).transform(self.tree)
        except Exception as e:
            self.tree = None
    
    @classmethod
    def operand_dict(cls, lines: list) -> OperandDict:
        res = OperandDict()
        for line in lines:
            for op in line.operands:
                res.add(op)
        res.randomize()
        return res

