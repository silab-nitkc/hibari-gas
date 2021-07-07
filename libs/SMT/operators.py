import z3
from ..GAS.parser import Parser
from ..static import *

class TypeA:
    """
    add, sub等の一般的な演算用の親クラス
    """
    def __init__(self, model):
        self.is_reg = model.is_reg
        self.dst = z3.BitVec('op{}-dst'.format(id(self)), REG_BITS)
        self.src = z3.BitVec('op{}-src'.format(id(self)), REG_BITS)

        self.src_is_imm = z3.BitVec('op{}-sii'.format(id(self)), 1) # 即値を使うなら1
        self.imm = z3.BitVec('op{}-imm'.format(id(self)), VAL_BITS)   # 即値の値
    
    def get_const(self, current, next, **kwargs):
        const = []

        dst, src, sii, imm, is_reg = self.dst, self.src, self.src_is_imm, self.imm, self.is_reg

        # サブクラスで定義された命令を埋め込む
        const += self.get_op_const(current, next)

        # ゼロフラグの設定
        const += [z3.If(next.val[dst] == 0, next.zero_flag == 1, next.zero_flag == 0)]

        # その他のレジスタは値を引き継ぐ
        const += [z3.If(dst != i, next.val[i] == current.val[i], True) for i in range(2**REG_BITS)]
        
        # プログラムカウンタを更新
        const += [next.pc == current.pc + 1]

        # 無意味な演算は禁止する
        const += [imm != 0, -10 <= imm, imm <= 10]

        # GASで不可能な演算（メモリ間演算）を禁止する
        const += [z3.Or(is_reg[dst] == 1, is_reg[src] == 1, sii == 1)]

        when = [current.op == self.ID]  # 自分自身が実行されているときのみ上記の制約を適用する
        return [z3.If(z3.And(when), z3.And(const), True)]
    
    def eval_as_long(self, m):
        sii = m.eval(self.src_is_imm).as_long()
        dst = m.eval(self.dst).as_long()

        if sii:
            imm = m.eval(self.imm).as_signed_long()
            return dst, sii, imm
        else:
            src = m.eval(self.src).as_long()
            return dst, sii, src
    
    def eval_as_GAS(self, m, gas_lines, i, suffix):
        try:
            sii = m.eval(self.src_is_imm).as_long()
            dst = m.eval(self.dst).as_long()
            if sii:
                imm = m.eval(self.imm).as_signed_long()
                gas_lines[i] += '{}{}\t${}, {{{}}}'.format(self.name, suffix, imm, dst)
            else:
                src = m.eval(self.src).as_long()
                gas_lines[i] += '{}{}\t{{{}}}, {{{}}}'.format(self.name, suffix, src, dst)
        except:
            pass

class Add(TypeA):
    ID = -1
    def __init__(self, model):
        super().__init__(model)

    def get_op_const(self, current, next):
        const = []
        dst, src, sii, imm = self.dst, self.src, self.src_is_imm, self.imm

        # 演算結果をレジスタに入れる
        const += [z3.If(sii == 0, 
                    next.val[dst] == current.val[dst] + current.val[src], 
                    next.val[dst] == current.val[dst] + imm
        )]

        return const
    
class Sub(TypeA):
    ID = -1
    def __init__(self, model):
        super().__init__(model)
    
    def get_op_const(self, current, next):
        const = []
        dst, src, sii, imm = self.dst, self.src, self.src_is_imm, self.imm

        # 演算結果をレジスタに入れる
        const += [z3.If(sii == 0, 
                    next.val[dst] == current.val[dst] - current.val[src], 
                    next.val[dst] == current.val[dst] - imm
        )]

        return const

class Mov:
    ID = -1
    def __init__(self, model):
        self.is_reg = model.is_reg
        self.dst = z3.BitVec('op{}-dst'.format(id(self)), REG_BITS)
        self.src = z3.BitVec('op{}-src'.format(id(self)), REG_BITS)

        self.src_is_imm = z3.BitVec('op{}-sii'.format(id(self)), 1)  # 即値を使うなら1
        self.imm = z3.BitVec('op{}-imm'.format(id(self)), VAL_BITS)   # 即値の値

    def get_const(self, current, next):
        const = []

        dst, src, sii, imm, is_reg = self.dst, self.src, self.src_is_imm, self.imm, self.is_reg

        # サブクラスで定義された命令を埋め込む
        const += self.get_op_const(current, next)

        # ゼロフラグの設定
        const += [next.zero_flag == current.zero_flag]

        # その他のレジスタは値を引き継ぐ
        const += [z3.If(dst != i, next.val[i] == current.val[i], True) for i in range(2**REG_BITS)]
        
        # プログラムカウンタを更新
        const += [next.pc == current.pc + 1]

        # 無意味な演算は禁止する
        const += [-10 <= imm, imm <= 10]

        # GASで不可能な演算（メモリ間演算）を禁止する
        const += [z3.Or(is_reg[dst] == 1, is_reg[src] == 1, sii == 1)]

        when = [current.op == self.ID]  # 自分自身が実行されているときのみ上記の制約を適用する
        return [z3.If(z3.And(when), z3.And(const), True)]

    def get_op_const(self, current, next):
        const = []
        dst, src, sii, imm = self.dst, self.src, self.src_is_imm, self.imm

        # 演算結果をレジスタに入れる
        const += [z3.If(sii == 0,
                        next.val[dst] == current.val[src],
                        next.val[dst] == imm
                        )]

        return const
    
    def eval_as_long(self, m):
        sii = m.eval(self.src_is_imm).as_long()
        dst = m.eval(self.dst).as_long()

        if sii:
            imm = m.eval(self.imm).as_signed_long()
            return dst, sii, imm
        else:
            src = m.eval(self.src).as_long()
            return dst, sii, src
            
    def eval_as_GAS(self, m, gas_lines, i, suffix):
        try:
            size = ''
            sii = m.eval(self.src_is_imm).as_long()
            dst = m.eval(self.dst).as_long()
            if sii:
                imm = m.eval(self.imm).as_signed_long()
                gas_lines[i] += '{}{}\t${}, {{{}}}'.format(self.name, suffix, imm, dst)
            else:
                src = m.eval(self.src).as_long()
                gas_lines[i] += '{}{}\t{{{}}}, {{{}}}'.format(self.name, suffix, src, dst)
        except:
            pass

class TypeB:
    """
        ジャンプ命令の親クラス
    """
    label_count = 0
    def __init__(self, model):
        self.PC_BITS = model.PC_BITS
        self.PC_LEN = model.PC_LEN
        self.imm = z3.BitVec('op{}-imm'.format(id(self)), model.PC_BITS)   # 即値の値

    def get_const(self, current, next, **kwargs):
        const = []
        
        imm = self.imm

        # サブクラスで定義された命令を埋め込む
        const += self.get_op_const(current, next)

        # 全レジスタ・フラグを引き継ぐ
        const += [next.val[i] == current.val[i] for i in range(2**REG_BITS)]
        const += [next.zero_flag == current.zero_flag]

        # ジャンプ先は命令列の範囲内とする
        const += [-current.pc <= imm, imm < self.PC_LEN - current.pc - 1, imm != 0, imm != 1]

        when = [current.op == self.ID]  # 自分自身が実行されているときのみ上記の制約を適用する
        return [z3.If(z3.And(when), z3.And(const), True)]
    
    def eval_as_long(self, m):
        imm = m.eval(self.imm).as_signed_long()
        return '---', '---', imm
    
    def eval_as_GAS(self, m, gas_lines, i, suffix):
        try:
            label_name = "L{}_{}".format(Parser.REC_COUNT, TypeB.label_count)
            TypeB.label_count += 1
            gas_lines[i] += "{}\t{}".format(self.name, label_name)

            imm = m.eval(self.imm).as_signed_long()
            gas_lines[i + imm] = label_name + ":\n" + gas_lines[i + imm]
        except:
            pass

class JZ(TypeB):
    ID = -1
    def __init__(self, model):
        super().__init__(model)

    def get_op_const(self, current, next, **kwargs):
        const = []
        
        # ゼロだったらジャンプする
        const += [z3.If(current.zero_flag == 1, next.pc == current.pc + self.imm, next.pc == current.pc + 1)]

        return const

class JNZ(TypeB):
    ID = -1
    def __init__(self, model):
        super().__init__(model)

    def get_op_const(self, current, next, **kwargs):
        const = []
        
        # ゼロでなければジャンプする
        const += [z3.If(current.zero_flag == 0, next.pc == current.pc + self.imm, next.pc == current.pc + 1)]

        return const

class Stop:
    """
    命令列の終端に設定する仮想命令
    この命令に到達したらプログラムを終了させる
    """
    ID = -1
    def __init__(self, model):
        self.PC_LEN = model.PC_LEN

    def get_const(self, current, next, **kwargs):
        const = []
        
        # PCを固定し，プログラムを中断させる
        const += [next.pc == current.pc]

        # 全レジスタ・フラグを引き継ぐ
        const += [next.val[i] == current.val[i] for i in range(2**REG_BITS)]
        const += [next.zero_flag == current.zero_flag]

        when = [current.op == self.ID]  # 自分自身が実行されているときのみ上記の制約を適用する
        return [z3.If(z3.And(when), z3.And(const), True)]

    def eval_as_long(self, m):
        return '---', 0, '---'

# 命令列生成時に用いる命令群
all = {
    'add': Add,
    'sub': Sub,
    'mov': Mov,
    'jz' : JZ,
    # 'jnz': JNZ,
    'stop': Stop,
}

BITS = len(bin(len(all.values()))) - 2

# 命令固有のIDを設定
for i, op in enumerate(all.values()):
    op.ID = i

# 命令の名前を設定
for name in all:
    all[name].name = name

# import code 
# code.InteractiveConsole(globals()).interact()
