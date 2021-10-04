from lark import Transformer

class Parser(Transformer):
    # recursive execution count
    REC_COUNT: int = 0
    def __init__(self, line):
        super().__init__()

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
    
    def xor(self, tree):
        self.line.op = 'xor'
    
    def and_(self, tree):
        self.line.op = 'and'
    
    def or_(self, tree):
        self.line.op = 'or'
    
    def mov(self, tree):
        self.line.op = 'mov'
    
    def jz(self, tree):
        self.line.op = 'jz'
        self.line.operands += [Operand(str(tree[0]))]
    
    def jnz(self, tree):
        self.line.op = 'jnz'
        self.line.operands += [Operand(str(tree[0]))]

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
        is_dummy = "R{}+".format(Parser.REC_COUNT) in tree[0]
        self.line.operands += [Operand(str(tree[0]), is_dummy=is_dummy)]
        return str(tree[0])

    def immidiate(self, tree):
        self.line.operands += [Operand(int(tree[0]),
                                       is_imm=True, val=int(tree[0]))]
        return int(tree[0])
