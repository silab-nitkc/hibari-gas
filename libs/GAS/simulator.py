from typing import Optional, Union
from lark import Transformer
from .line import Line
from .operand import OperandDict
from random import randint, seed
seed(0)

class Simulator(Transformer):
    def __init__(self, op_dict: OperandDict) -> None:
        super().__init__()
        self.op_dict = op_dict
        self.pc = 0
        self.zf = randint(0, 1)
        self.jump_to = None
    
    def suffix_to_int(self, suffix: str) -> int:
        return 2**self.suffix_to_bits(suffix)

    def suffix_to_bits(self, suffix: str) -> int:
        return {
            'q': 64,
            'l': 32,
        }[suffix]
    
    def exp(self, tree):
        pass

    def label(self, tree):
        self.pc += 1
    
    def add(self, tree):
        self.op_dict.all[tree[2]].val += self.op_dict.all[tree[1]].val
        temp = self.op_dict.all[tree[2]].val % self.suffix_to_int(tree[0])
        self.zf = 1 if temp == 0 else 0
        self.pc += 1

    def sub(self, tree):
        self.op_dict.all[tree[2]].val -= self.op_dict.all[tree[1]].val
        temp = self.op_dict.all[tree[2]].val % self.suffix_to_int(tree[0])
        self.zf = 1 if temp == 0 else 0
        self.pc += 1
    
    def xor(self, tree):
        self.op_dict.all[tree[2]].val ^= self.op_dict.all[tree[1]].val
        temp = self.op_dict.all[tree[2]].val % self.suffix_to_int(tree[0])
        self.zf = 1 if temp == 0 else 0
        self.pc += 1
    
    def and_(self, tree):
        self.op_dict.all[tree[2]].val &= self.op_dict.all[tree[1]].val
        temp = self.op_dict.all[tree[2]].val % self.suffix_to_int(tree[0])
        self.zf = 1 if temp == 0 else 0
        self.pc += 1
    
    def or_(self, tree):
        self.op_dict.all[tree[2]].val |= self.op_dict.all[tree[1]].val
        temp = self.op_dict.all[tree[2]].val % self.suffix_to_int(tree[0])
        self.zf = 1 if temp == 0 else 0
        self.pc += 1

    def mov(self, tree):
        self.op_dict.all[tree[2]].val = self.op_dict.all[tree[1]].val
        self.pc += 1

    def jz(self, tree):
        if self.zf == 1:
            self.pc = tree[0]
        else:
            self.pc += 1

    def jnz(self, tree):
        if self.zf == 0:
            self.pc = tree[0]
        else:
            self.pc += 1
            
    def suffix(self, tree):
        return str(tree[0])

    def operand(self, tree):
        return tree[0]

    def x64register(self, tree):
        return str(tree[0])

    def x32register(self, tree):
        return str(tree[0])

    def name(self, tree):
        return str(tree[0])
    
    def dummy(self, tree):
        return str(tree[0])

    def immidiate(self, tree):
        return int(tree[0])

def find_label(lines: list[Line], label: str):
    for i, line in enumerate(lines):
        if line.label == label:
            return i
    return None

def simulate(lines: list[Line], start: Optional[OperandDict] = None) -> list[Union[OperandDict, Simulator]]:
    """GASの挙動をシミュレートする

    Lineインスタンスのリストを受け取り，実行前後のオペランドの値とプログラムカウンタ等の値を返す．

    Args:
        lines (list[Line]):  実行するGAS（Line）のリスト
        start (OperandDict, optional):  オペランドの初期値（指定がなければ乱数を用いる）
    """
    if start is None:
        start   = Line.operand_dict(lines)

    end     = start.copy()
    sim     = Simulator(end)
    for i in range(100):
        try:
            line = lines[sim.pc]
        except:
            break
        sim.transform(line.tree)

        # 指定されたラベルにジャンプする
        if type(sim.pc) is not int:
            sim.pc = find_label(lines, sim.pc)
    else:
        # ここまで到達したら無限ループであるとみなす
        return None, None, None
    return start, end, sim
