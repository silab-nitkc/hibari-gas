# hibari

*hibari*は，Man-at-the-end攻撃からソフトウェアを保護することを目的とした難読化ツールです．
GNU assembler形式のアセンブリプログラムを入力とし，
難読化されたアセンブリプログラムを出力します．
難読化対象のプログラムに含まれるいくつかのコード断片（命令列）は，
その意味を保ったまま不明瞭な表現に置換されます．
不明瞭な表現を持つコードは，SMTソルバであるZ3を用いて自動生成されます．

## 仕組み
具体的には，hibariは，入力されたアセンブリプログラムについて，
次の手順を繰り返し適用することで難読化を行います．

1. 置換対象のコード断片を選択し，構文解析を通してその入出力例を求める
1. SMTソルバを用いて，入出力例を満たす任意長の新しいコード断片（命令列）を求める
1. 新しいコード断片をGAS形式に整形し，それに対して多数の入出力例を用いたテストを行う．パスできなければ1.へ戻る．
1. 置換対象コードを，生成された新しいコードに置換する

## Requirements
* Python 3.9 (or higher)
* z3py
* lark-python

## Usage
```
usage: obfuscator.py [-h] [-o O] [-n N] [-l L] src

positional arguments:
  src         Path of input file.

optional arguments:
  -h, --help  show this help message and exit
  -o O        Path of output file.
  -n N        Maximum number of lines to obfuscate at once.
  -l L        Number of instructions used for obfuscation.
```

### Example
```bash
python3.9 obfuscator.py target.s -o out.s
```

## Reference
光本智洋，神崎雄一郎，&ldquo; SMTソルバによる命令列生成を用いたアセンブリプログラムの難読化，&rdquo; 情報処理学会 第83回全国大会講演論文集 (講演番号2K-04)，2021年3月．
