from .parser import parse, Parser
from .line import Line
from .simulator import Simulator
import z3
import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from code_generator import *  # noqa


class Obfuscator:
    def __init__(self, raw: str, all_instructions: list[str]):
        self.raw: str = raw
        self.lines: list[Line] = list(map(parse, raw.split("\n")))
        self.all_instructions: list[str] = all_instructions

    def run(self, MAX_LINE_N: int = 1) -> str:
        target_list: list[Line] = []
        res: list[str] = []

        for line in self.lines:
            if line.is_obfuscatable(self.all_instructions):
                target_list += [line]
                continue
            elif len(target_list):
                res += self.obfuscate(target_list, 5, 2)
                target_list = []

            if len(target_list) >= MAX_LINE_N:
                res += self.obfuscate(target_list, 5, 2)
                target_list = []
            else:
                res += [line.raw]

        return res

    def obfuscate(self, lines: list[Line], inst_N: int, tl_N: int) -> list[str]:
        simulator: Simulator = Simulator(lines)

        const: list = []
        inst_seq = InstructionSequence()
        for i in range(inst_N):
            inst_seq.add_instruction(Instruction(all))

        for i in range(tl_N):
            init_operands: dict
            operands: dict
            init_operands, operands = simulator.run()

            in_values: list = (list(init_operands.values()) +
                               [None for i in range(2**REG_BITS)])[:2**REG_BITS]

            out_values: list[int] = (list(operands.values()) +
                                     [None for i in range(2**REG_BITS)])[:2**REG_BITS]

            tl: Timeline = Timeline(inst_N+1)
            const += tl.get_state(0).set_values(in_values)
            const += tl.get_state(inst_N).set_values(out_values)
            const += tl.get_const()
            const += inst_seq.instructions[0].get_const(
                tl.get_state(0), tl.get_state(1))

        sl = z3.Solver()
        sl.add(const)
        if sl.check() == z3.unsat:
            print("unsat!")
            return lines

        result: list[dict] = []
        for inst in inst_seq.instructions:
            result += [inst.eval(m)]

        return result
