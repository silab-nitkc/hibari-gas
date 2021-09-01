# hibari
[ [English](README.md) | [日本語](README.ja.md) ]

*hibari* is an experimental obfuscator for the assembly language, which aims to protect software against Man-at-the-end attacks.
Hibari takes an assembly program (in the GNU assembler format) as input, and returns an obfuscated assembly program as output.
In hibari, some code fragments included in the target program are replaced with *obscure* fragments, preserving their semantics. The obscure fragments are generated using an SMT solver Z3.

(figure)

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
