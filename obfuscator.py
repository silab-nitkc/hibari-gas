from libs.SMT.core import IOExample, Values, Model
from libs.GAS.simulator import simulate
from libs.GAS.line import Line
from libs.GAS.parser import Parser
from libs.GAS.operand import OperandDict
from libs.static import *
import re, random, argparse
from copy import deepcopy

parser = argparse.ArgumentParser(description="GAS obfuscator.")

parser.add_argument('src', help='Path of input file.')
parser.add_argument('-o', help='Path of output file.', default='res.s')
parser.add_argument('-n', help='Maximum number of lines to obfuscate at once.', default=2, type=int)
parser.add_argument('-l', help='Number of instructions used for obfuscation.', default=5, type=int)

args = parser.parse_args()

with open(args.src, 'r', encoding='utf-8') as f:
    raw = f.read()

lines = list(map(Line, raw.split('\n')))

def ignore_imm(op_dict: OperandDict) -> OperandDict:
    res = OperandDict()
    for i in op_dict.all.keys():
        if type(i) is int:
            continue
        res.add(op_dict.all[i])
    
    return res

def obfuscate(lines):
    op_dict = Line.operand_dict(lines)
    ioe = []
    for i in range(3):
        init, res, sim = simulate(lines, op_dict)
        vals = [Values([i.val for i in ignore_imm(init).all.values()], start=True)]
        vals += [Values() for i in range(args.l+1)]
        vals += [Values([i.val for i in ignore_imm(res).all.values()], end=True)]
        ioe += [IOExample(vals)]
    
    is_reg = [1 if i.is_reg else 0 for i in ignore_imm(init).all.values()]
    model = Model(ioe, args.l, is_reg, Parser.REC_COUNT)

    if (m:=model.solve()) is None:
        pass

    op_code = [m.eval(model.op[i]).as_long() for i in range(args.l)]
    op_list = model.op_list
    res = ['' for i in range(args.l)]

    for i in range(args.l):
        op = op_list[i].op_list[op_code[i]]
        op.eval_as_GAS(m, res, i, lines[0].suffix)
    
    res2 = []
    for r in res:
        if r == '':
            continue
        res2 += [r]

    return '\n'.join(res2).format(*list(ignore_imm(init).all.keys()) + [r'R{}+{}*8(%rip)'.format(Parser.REC_COUNT, i) for i in range(16)])

def check(lines1: list[Line], lines2: list[Line]):
    for i in range(1000):
        op1 = Line.operand_dict(lines1)
        op2 = Line.operand_dict(lines2)
        if i == 0:
            for op in op2.all.values():
                op.val = op.val if op.is_imm else 0
        OperandDict.extend(op1, op2)

        init1, res1, sim1 = simulate(lines1, op1)
        import code
        # code.InteractiveConsole(locals()).interact()
        init2, res2, sim2 = simulate(lines2, op2)
        if not ignore_imm(res1).same_as(res2):
            return False
    
    return True

out = ".data\nR{}: .space 160\n".format(Parser.REC_COUNT)
for line in lines:
    print("\033[33m[Pending]\033[0m\t" + line.raw)
    print("\033[1A", end='')
    if line.op and line.op not in ['jz', 'jnz']:
        done = False
        for i in range(10):
            res = obfuscate([line])
            res_lines = list(map(Line, res.split('\n')))
            if check([line], res_lines):
                out += res + '\n'
                print("\033[32m[Obfuscated]\t\033[31m" + line.raw + "\033[0m")
                for l in res_lines:
                    print("\t\033[32m\t" + l.raw + "\033[0m")
                done = True
                break
        if done:
            continue
    out += line.raw + '\n'
    print("\033[32m[Skiped] \033[0m\t" + line.raw)

with open(args.o, 'w', encoding='utf-8') as f:
    f.write(out)
