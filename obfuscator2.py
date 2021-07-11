from libs.GAS import *
from libs.SMT import *
from libs.settings import *
from libs import color
from typing import Tuple
import argparse

def obfuscate(lines: list[Line], OP_LEN: int, ttl: int = 3) -> Tuple[list[Line], bool]:
    """難読化関数

    Lineインスタンスのリストを受け取り，難読化したLineインスタンスのリストを返す．
    難読化に失敗した場合，受け取ったリストをそのまま返す．

    Args:
        line (Line[]): 難読化対象のGAS
        OP_LEN (int): 命令列の長さ
        ttl (int, optional): 難読化を試行する最大回数
    """

    if ttl <= 0:
        return lines, False

    # 入出力例のリスト
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
        return lines, False
    
    return merge(model, lines), True

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

    for i, line in enumerate(lines):
        print(f'{color.yellow}[Pending]{color.reset}\t{line.raw}')

        if line.op not in TARGET_OP:
            res += [line]
            color.back_to(1)
            print(f'[ {i+1}/{len(lines)} ]\t{line.raw}')
            continue
        
        obfuscated_lines, succeded = obfuscate([line], args.l)
        res += obfuscated_lines
        
        color.back_to(1)
        if succeded:
            print(f'{color.green}[Obfuscated]{color.red}\t{line.raw}{color.reset}')
            for l in obfuscated_lines:
                print(f'{color.green}    |--> \t{l.raw}{color.reset}')
        else:
            print(f'[ {i+1}/{len(lines)} ]\t{line.raw}')
    
    res = insert_data(lines)
    
    with open(args.o, 'w', encoding='utf-8') as f:
        f.write('\n'.join([l.raw for l in res]) + '\n')

if __name__ == "__main__":
    main()
