from . import Line, OperandDict, Operand, Parser
from ..SMT import Model
from copy import deepcopy

# 自動生成されるジャンプ先の個数
LABEL_COUNT = 0

def typeA(model: Model, operands: OperandDict, op, suffix: str) -> Line:
    dst, sii, src = op.eval_as_long(model.m)
    if dst is None:
        return Line('')

    if sii == 1:
        src = '$' + str(src)
    else:
        src = list(operands.ignore_imm().all.values())[src].name
    dst = list(operands.ignore_imm().all.values())[dst].name
    res = '\t{op}{suffix}\t{src}, {dst}'.format(op = op.name, suffix = suffix, src = src, dst = dst)
    
    return Line(res)

def typeB(model: Model, operands: OperandDict, op, suffix: str) -> Line:
    imm = op.eval_as_long(model.m)
    if imm is None:
        return Line('')

    res = f'\t{op.name}\t{imm}'
    return Line(res)

builder = {
    'add': typeA,
    'sub': typeA,
    'xor': typeA,
    'or' : typeA,
    'and': typeA,
    'mov': typeA,
    'jz' : typeB,
    'jnz': typeB,
}

def merge(model: Model, lines: list[Line]) -> list[Line]:
    global LABEL_COUNT
    res: list[Line] = [Line('') for i in range(model.PC_LEN-1)]
    op_dict = Line.operand_dict(lines).ignore_imm()
    for i in range(2**model.PC_BITS - len(op_dict.all)):
        op_dict.add(Operand('R{}+{}*8(%rip)'.format(Parser.REC_COUNT, i), is_dummy=True))

    op_list = model.op_list
    for i in range(model.PC_LEN - 1):
        op = op_list[i].op_list[model.m.eval(model.op[i]).as_long()]
        res[i] = builder[op.name](model, op_dict, op, lines[0].suffix)
    # ジャンプ先
    labels: list[list[Line]] = [[] for i in range(model.PC_LEN-1)]
    for i, line in enumerate(res):
        if line.op not in ['jz', 'jnz']:
            continue
        diff = int(line.operands[0].name)
        label = f'L{Parser.REC_COUNT}_{LABEL_COUNT}'
        labels[i+diff] += [Line(f'{label}:')]
        res[i] = Line(res[i].raw.replace(line.operands[0].name, label))
        LABEL_COUNT += 1
    
    res2:list[Line] = []
    for i in range(model.PC_LEN-1):
        res2 += labels[i]
        res2 += [res[i]]

    res2 += [Line(f'\tadd{lines[-1].suffix}\t$0, {lines[-1].operands[-1].name}')]    
    return list(filter(lambda x: x.raw != '', res2))

def insert_data(lines: list[Line]) -> list[Line]:
    res = [Line('.data'), Line('R{}: .space 160'.format(Parser.REC_COUNT))]
    return res + lines
