from lark import Transformer, Lark
from .line import Line
import os
import sys
from random import randint

with open(os.path.dirname(__file__) + '/../gas_obfuscator/gas.lark', encoding="utf-8") as g:
    lark_parser = Lark(g.read(), start="exp")


class Simulator:
    def __init__(self, lines: list[Line]) -> None:
        self.lines: list[Line] = lines

    def run(self, init_values: dict = {}) -> list[dict, dict]:
        pc: int = -1

        temp: dict = Line.get_operands(self.lines)
        init_operands: dict = self.randomize_dict(temp)
        init_operands.update(init_values)

        operands: dict = init_operands.copy()

        for ttl in range(99, -1, -1):
            pc += 1
            if pc >= len(self.lines):
                break

            line: Line = self.lines[pc]

            if not line.op:
                continue

            src = operands[line.src] if not line.src_is_immediate else line.immediate
            if line.op == "add":
                operands[line.dst] += src
            if line.op == "sub":
                operands[line.dst] -= src
            if line.op == "xor":
                operands[line.dst] ^= src
            if line.op == "or":
                operands[line.dst] |= src
            if line.op == "and":
                operands[line.dst] &= src
            if line.op == "mov":
                operands[line.dst] = src
        else:
            return None
        return init_operands, operands

    def randomize_dict(self, target: dict) -> dict:
        res: dict = target.copy()
        for key in res:
            res[key] = randint(0, 255)

        return res
