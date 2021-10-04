from typing import TYPE_CHECKING
import z3
from .state import State
from .const import *


class Instruction:
    _counter = 0

    def __init__(self, instructions: list) -> None:
        self.all_instructions = [instruction(
            self) for instruction in instructions]

        self.op_id = z3.BitVec(
            f'Instruction/{Instruction._counter}/op_id', OP_BITS)
        self.dst = z3.BitVec(
            f'Instruction/{Instruction._counter}/dst', REG_BITS)
        self.src = z3.BitVec(
            f'Instruction/{Instruction._counter}/src', REG_BITS)
        self.src_is_immediate = z3.BitVec(
            f'Instruction/{Instruction._counter}/sii', 1)
        self.immediate = z3.BitVec(
            f'Instruction/{Instruction._counter}/imm', VAL_BITS)
        Instruction._counter += 1

    def get_const(self, current: State, next: State):
        const = sum(map(lambda inst: inst.get_const(current, next), self.all_instructions), [])
        const += [self.op_id >= 0, self.op_id < len(self.all_instructions)]
        return const
    
    def eval(self, model) -> dict:
        res = {
            "instruction_id": model.eval(self.op_id).as_long(),
            "instruction": self.all_instructions[model.eval(self.op_id).as_long()].__class__.__name__,
            "dst": model.eval(self.dst).as_long(),
            "src_is_immediate": model.eval(self.src_is_immediate).as_long(),
            "src": None,
            "immediate": None,
        }

        if res["src_is_immediate"]:
            res["immediate"] = model.eval(self.immediate).as_long()
        else:
            res["src"] = model.eval(self.src).as_long()

        return res
