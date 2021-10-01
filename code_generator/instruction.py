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
        return sum(map(lambda inst: inst.get_const(current, next), self.all_instructions), [])
