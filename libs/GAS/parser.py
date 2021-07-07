from lark import Transformer
from .operand import Operand

class Parser(Transformer):
    # recursive execution count
    REC_COUNT: int = 0
    def __init__(self, line):
        super().__init__()
        self.line = line

    def suffix_to_int(self, suffix):
        return {
            "q": 2**64,
            "l": 2**32,
        }[suffix]

    def exp(self, tree):
        pass

    def arr_label(self, tree):
        Parser.REC_COUNT += 1

    def label(self, tree):
        self.line.label = str(tree[0])

    def add(self, tree):
        self.line.op = 'add'

    def sub(self, tree):
        self.line.op = 'sub'
    
    def mov(self, tree):
        self.line.op = 'mov'
    
    def jz(self, tree):
        self.line.op = 'jz'
    
    def jnz(self, tree):
        self.line.op = 'jnz'

    def suffix(self, tree):
        self.line.bits = self.suffix_to_int(tree[0])
        self.line.suffix = tree[0]

    def operand(self, tree):
        return tree[0]

    def x64register(self, tree):
        self.line.operands += [Operand(str(tree[0]), is_reg=True, bits=64)]
        return str(tree[0])

    def x32register(self, tree):
        self.line.operands += [Operand(str(tree[0]), is_reg=True, bits=32)]
        return str(tree[0])

    def name(self, tree):
        self.line.operands += [Operand(str(tree[0]))]
        return str(tree[0])
    
    def dummy(self, tree):
        is_dummy = "R{}+".format(self.REC_COUNT) in tree[0]
        self.line.operands += [Operand(str(tree[0]), is_dummy=is_dummy)]
        return str(tree[0])

    def immidiate(self, tree):
        self.line.operands += [Operand(int(tree[0]),
                                       is_imm=True, val=int(tree[0]))]
        return int(tree[0])
