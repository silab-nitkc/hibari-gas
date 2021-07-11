from . import Line, OperandDict, Operand, Parser
from ..SMT import Model
from copy import deepcopy

def typeA(model: Model, operands: OperandDict, op, suffix: str) -> Line:
    dst, sii, src = op.eval_as_long(model.m)
    if sii == 1:
        src = '$' + str(src)
    else:
        src = list(operands.ignore_imm().all.values())[src].name
    dst = list(operands.ignore_imm().all.values())[dst].name
    res = '\t{op}{suffix}\t{src}, {dst}'.format(op = op.name, suffix = suffix, src = src, dst = dst)
    
    return Line(res)

builder = {
    'add': typeA,
    'sub': typeA,
    'xor': typeA,
    'or' : typeA,
    'and': typeA,
    'mov': typeA,
}

def merge(model: Model, lines: list[Line]) -> list[Line]:
    res: list[Line] = [Line('') for i in range(model.PC_LEN-1)]
    op_dict = Line.operand_dict(lines).ignore_imm()
    for i in range(2**model.PC_BITS - len(op_dict.all)):
        op_dict.add(Operand('R{}+{}*8(%rip)'.format(Parser.REC_COUNT, i), is_dummy=True))

    op_list = model.op_list
    for i in range(model.PC_LEN - 1):
        op = op_list[i].op_list[model.m.eval(model.op[i]).as_long()]
        res[i] = builder[op.name](model, op_dict, op, lines[0].suffix)

    return res

def insert_data(lines: list[Line]) -> list[Line]:
    res = [Line('.data'), Line('R{}: .space 160'.format(Parser.REC_COUNT))]
    return res + lines