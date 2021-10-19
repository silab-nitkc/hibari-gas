import argparse
from gas_obfuscator.obfuscator import Obfuscator


def main():
    parser = argparse.ArgumentParser(description='GAS obfuscator.')
    parser.add_argument('src', help='Path of input file.')
    parser.add_argument('-o', help='Path of output file.', default='res.s')
    parser.add_argument(
        '-n', help='[Experimental] Maximum number of lines to obfuscate at once.', default=1, type=int)
    parser.add_argument(
        '-l', help='Number of instructions used for obfuscation.', default=5, type=int)
    parser.add_argument('--rangediv', action="store_true",
                        help='Use range divider.')

    args = parser.parse_args()

    with open(args.src, 'r', encoding='utf-8') as f:
        raw = f.read()

    obfuscator: Obfuscator = Obfuscator(raw, ["add", "sub"])
    res = obfuscator.run(MAX_LINE_N=args.n, inst_N=args.l,
                         tl_N=20, use_range_divider=args.rangediv)

    with open(args.o, 'w', encoding='utf-8') as f:
        f.writelines([i + '\n' for i in res])


if __name__ == "__main__":
    main()
