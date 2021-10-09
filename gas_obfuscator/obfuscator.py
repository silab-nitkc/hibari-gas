from gas_obfuscator.generator import GASGenerator
from .parser import parse, Parser
from .line import Line
from .simulator import Simulator
import z3
import sys
import os
import random
import string

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from code_generator import *  # noqa


class Obfuscator:
    def __init__(self, raw: str, all_instructions: list[str]):
        self.raw: str = raw
        self.lines: list[Line] = list(map(parse, raw.split("\n")))
        self.all_instructions: list[str] = all_instructions
        self.label_name = self._get_label_name()

    def run(self, MAX_LINE_N: int = 1, inst_N: int = 5, tl_N: int = 2) -> str:
        target_list: list[Line] = []
        res: list[str] = []
        res += [f".data"]
        res += [f"{self.label_name}: .space 160"]

        for line in self.lines:
            if line.is_obfuscatable(self.all_instructions):
                target_list += [line]
            elif len(target_list):
                res += self.obfuscate(target_list, inst_N, tl_N)
                target_list = []

            if len(target_list) >= MAX_LINE_N:
                res += self.obfuscate(target_list, inst_N, tl_N)
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
            const += tl.get_state(0).set_values(in_values, randomize=True)
            const += tl.get_state(inst_N).set_values(out_values)
            const += tl.get_const()

            for j in range(inst_N):
                const += inst_seq.instructions[j].get_const(
                    tl.get_state(j), tl.get_state(j + 1))
                const += self._get_memory_refs_const(
                    lines, inst_seq.instructions[j])

        sl = z3.Solver()
        sl.add(const)
        if sl.check() == z3.unsat:
            print("unsat!")
            return lines

        m = sl.model()
        generated_instructions: list[dict] = list(
            map(lambda inst: inst.eval(m), inst_seq.instructions))
        operand_names: list[str] = list(
            operands.keys()) + [f"{self.label_name}+{j}*8(%rip)" for j in range(2**REG_BITS)]
        generated_lines: list[Line] = Line.convert_to_lines(
            generated_instructions, operand_names, lines[0].suffix)
        return [i.raw for i in generated_lines]

    def _get_label_name(self):
        for i in range(100):
            temp = ''.join(random.choices(string.ascii_letters, k=5))
            if temp not in self.raw:
                break
        else:
            print("error!")
        return temp

    def _get_memory_refs_const(self, lines: list[Line], inst: Instruction) -> list:
        has_memory_ref: list[bool] = list(
            Line.get_operands_with_memory_ref(lines).values()) + [True for i in range(2**REG_BITS)]

        res = []
        for i in range(2**REG_BITS):
            if not has_memory_ref[i]:
                continue
            for j in range(2**REG_BITS):
                if has_memory_ref[j]:
                    res += [inst.src != j]
        print(res)
        return res
