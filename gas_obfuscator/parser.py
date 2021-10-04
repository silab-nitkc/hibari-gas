from lark import Transformer
from .line import Line
import sys

class Parser(Transformer):
    # recursive execution count
    REC_COUNT: int = 0
    def __init__(self, line: Line):
        super().__init__()
        self.line = line

    def exp(self, tree):
        pass

    def arr_label(self, tree):
        pass

    def label(self, tree):
        self.line.label = str(tree[0])

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
            "name": str(tree[0]),
            "has_memory_ref": False,
            "is_immediate": True,
        }
