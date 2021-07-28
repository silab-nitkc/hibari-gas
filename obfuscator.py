from libs.GAS import *
from libs.SMT import *
from libs.settings import *
from libs import color
from typing import Tuple
import argparse

def check(lines1: list[Line], lines2: list[Line]) -> bool:
    for i in range(TEST_N):
        op1 = Line.operand_dict(lines1)
        op2 = Line.operand_dict(lines2)
        OperandDict.extend(op1, op2)

        start1, end1, flag1 = simulate(lines1, op1)
        start2, end2, flag2 = simulate(lines2, op2)
        if start1 is None or start2 is None:
            return False
        if not end1.ignore_imm().same_as(end2.ignore_imm()):
            return False

    return True

def obfuscate(lines: list[Line], OP_LEN: int, retry: int = 0) -> Tuple[list[Line], bool]:
    """難読化関数

    Lineインスタンスのリストを受け取り，難読化したLineインスタンスのリストを返す．
    難読化に失敗した場合，受け取ったリストをそのまま返す．

    Args:
        line (Line[]): 難読化対象のGAS
        OP_LEN (int): 命令列の長さ
        ttl (int, optional): 難読化を試行する最大回数
    """

    if retry >= RETRY_MAX:
        return lines
    
    if retry == 0:
        for line in lines:
            print(f'{color.red} - {line.raw}{color.reset}')

    # 入出力例
    ioexamples: list[IOExample] = []

    for i in range(IOExample_N):
        start, end, _ = simulate(lines)
        start = start.ignore_imm()
        end   = end.ignore_imm()
        values = [Values(start.get_values(), start=True)]
        values += [Values() for i in range(OP_LEN)]
        values += [Values(end.get_values(), end=True)]
        ioexamples += [IOExample(values)]
        
    is_reg = [op.is_reg for op in start.ignore_imm().all.values()]
    model = Model(ioexamples, OP_LEN, is_reg)

    if (m:=model.solve()) is None:
        return lines
    
    res = merge(model, lines)

    # 入出力テスト
    if not check(lines, res):
        return obfuscate(lines, OP_LEN, retry+1)
    
    return res

def main():
    parser = argparse.ArgumentParser(description='GAS obfuscator.')
    parser.add_argument('src', help='Path of input file.')
    parser.add_argument('-o', help='Path of output file.', default='res.s')
    parser.add_argument('-n', help='Maximum number of lines to obfuscate at once.', default=2, type=int)
    parser.add_argument('-l', help='Number of instructions used for obfuscation.', default=5, type=int)

    args = parser.parse_args()

    with open(args.src, 'r', encoding='utf-8') as f:
        raw = f.read()
    
    lines: list[Line] = list(map(Line, raw.split('\n')))
    res  : list[Line] = []
    buf  : list[Line] = []

    for i, line in enumerate(lines):
        if line.op not in TARGET_OP:
            if len(buf) != 0:
                print(f'{args.src}:{i}')
                temp = obfuscate(buf, args.l)
                for line in temp:
                    print(f'{color.green} + {line.raw}{color.reset}')
                res += temp
                buf = []
            res += [line]
            continue
        
        buf += [line]
        
        if len(buf) < MAX_LINE_N:
            continue

        print(f'{args.src}:{i+1}')
        temp = obfuscate(buf, args.l)
        for line in temp:
            print(f'{color.green} + {line.raw}{color.reset}')
        res += temp
        buf = []
    
    res = insert_data(res)
    
    with open(args.o, 'w', encoding='utf-8') as f:
        f.write('\n'.join([l.raw for l in res]) + '\n')

if __name__ == "__main__":
    main()
