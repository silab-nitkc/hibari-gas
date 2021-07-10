from typing import Union
from random import randint
from copy import deepcopy

class Operand:
    def __init__(self, name, is_reg=False, is_imm=False, is_dummy=False, val=None, bits: int = 64):
        self.name = name
        self.is_reg = is_reg
        self.is_imm = is_imm
        self.is_dummy = is_dummy
        self.bits = bits
        self.val = val
    
class OperandDict:
    def __init__(self) -> None:
        self.all: dict[str, Operand] = {}
        self.randomize()

    def randomize(self) -> None:
        for op in self.all.values():
            op.val = op.val if op.is_imm else randint(-31, 31)
    
    def copy(self):
        return deepcopy(self)
    
    def same_as(self, op_dict) -> bool:
        for key in self.all:
            if key not in op_dict.all:
                continue
            if self.all[key].val != op_dict.all[key].val:
                return False
        return True
    
    def add(self, op: Operand) -> None:
        if op.name not in self.all:
            self.all[op.name] = op
        
    def ignore_dummies(self):
        """難読化によって自動生成された変数を除いたOperandDictを返す．
        """
        res = OperandDict()
        for op in self.all.values():
            if op.is_dummy:
                continue
            res.add(op)
        return res
    
    def ignore_imm(self):
        """即値を除いたOperandDictを返す．
        """
        res = OperandDict()
        for op in self.all.values():
            if op.is_imm:
                continue
            res.add(op)
        return res
    
    def get_values(self):
        return [op.val for op in self.all.values()]

    @staticmethod
    def extend(op1, op2) -> None:
        for key in op1.all:
            if key in op2.all:
                op1.all[key].val = op2.all[key].val
