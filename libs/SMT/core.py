import z3
from random import randint
from . import operators
from ..static import *

class Model:
    def __init__(self, ioe, PC_LEN, is_reg):
        """
            ioe: IOExampleの配列．
            PC_LEN: 命令列の長さ．
            is_reg: レジスタならTrue，それ以外ならFalseを入れる．
        """
        self.PC_LEN     = PC_LEN + 1
        self.PC_BITS    = len(bin(self.PC_LEN)) - 2
        self.step_len   = len(ioe[0].values)
        self.step_bits  = len(bin(self.step_len)) - 2

        self.is_reg = z3.Array('is_reg', z3.BitVecSort(REG_BITS), z3.BitVecSort(1))
        self.ioe = ioe

        self.op = z3.Array('op', z3.BitVecSort(self.PC_BITS), z3.BitVecSort(operators.BITS))
        self.op_list = [Op(self, pc) for pc in range(self.PC_LEN)]
        self.sl = z3.Solver()

        const = []
        for ioe in self.ioe:
            const += ioe.get_const(self)
        
        for i in range(self.PC_LEN - 1):
            const += [z3.ULE(0, self.op[i]), z3.ULT(self.op[i], len(operators.all.values()) - 1)] 

        for i in range(2**REG_BITS):
            if len(is_reg) > i:
                const += [self.is_reg[i] == (1 if is_reg[i] else 0)]
            else:
                const += [self.is_reg[i] == 0]
        
        const += [self.op[self.PC_LEN - 1] == operators.Stop.ID]
        self.sl.add(const)
    
    def solve(self):
        if self.sl.check() == z3.unsat:
            print('unsat')
            return None
        m = self.sl.model()
        self.m = m
        return m

class IOExample:
    def __init__(self, values):
        """
            values: valuesクラスの配列
        """
        self.values = values
    
    def get_const(self, model):
        const = []
        for val in self.values:
            # 入出力例に命令をセット
            val.set_model(model)
            # 入出力例ごとに制約を取得する
            const += val.get_const()

        for i, val in enumerate(self.values[:-1]):
            for op in model.op_list:
                const += op.get_const(self.values[i], self.values[i+1])
        
        return const

class Values:
    def __init__(self, val_example = None, start = False, end = False):
        """
            val_example:    各レジスタの値のint型配列．指定しないならNone
            start:          プログラムの初期状態ならTrueを設定する
            end:            プログラムの終端ならTrueを設定する
        """
        self.val = z3.Array('val{}'.format(id(self)), z3.BitVecSort(REG_BITS), z3.BitVecSort(VAL_BITS))
        self.zero_flag = z3.BitVec('zf{}'.format(id(self)), 2)
        self.val_example = val_example
        self.start = start
        self.end = end
    
    def set_model(self, model):
        self.model = model
        self.PC_LEN = model.PC_LEN
        self.PC_BITS = model.PC_BITS
        self.pc = z3.BitVec('pc{}'.format(id(self)), self.PC_BITS)
        self.op = model.op[self.pc]

    def get_const(self):
        ret = []
        if self.val_example is not None:
            for i,ex in enumerate(self.val_example):
                ret += [self.val[i] == ex]
        
        # プログラムの終端なら最後の命令(Stop)を実行する
        if self.end:
            ret += [self.pc == self.PC_LEN - 1]
        elif self.start:
            ret += [self.pc == 0]
            # 最初からジャンプされるとフラグの値が不明なため禁止しておく
            ret += [self.zero_flag == 2]
            for i in range(len(self.val_example), 2**REG_BITS):
                ret += [self.val[i] == randint(0, 2**VAL_BITS)]
        else:
            ret += [z3.ULE(0, self.pc), z3.ULE(self.pc, self.PC_LEN - 1)]

        return ret

class Op:
    """
        プログラムカウンタPCがある値となった時点の命令を定義するクラス
    """
    def __init__(self, model, PC):
        """
            PC: この命令を実行する際のプログラムカウンタの値(int)
        """
        self.PC = PC
        self.model = model
        self.op_list = [op(model) for op in operators.all.values()]
    
    def get_const(self, current, next):
        ret = []
        for op in self.op_list:
            ret += op.get_const(current, next)
        
        const = [current.pc == self.PC]
        return [z3.If(z3.And(const), z3.And(ret), True)]
