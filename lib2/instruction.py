from typing import TYPE_CHECKING
import z3
from state import State

OP_BITS = 4
REG_BITS = 2
VAL_BITS = 8

class Instruction:
    _counter = 0
    def __init__(self, instructions: list) -> None:
        self.all_instructions = [instruction(self) for instruction in instructions]

        self.op_id = z3.BitVec(f'Instruction/{Instruction._counter}/op_id/{id(self)}', OP_BITS)
        self.dst = z3.BitVec(f'Instruction/{Instruction._counter}/dst/{id(self)}', REG_BITS)
        self.src = z3.BitVec(f'Instruction/{Instruction._counter}/src/{id(self)}', REG_BITS)
        self.src_is_immediate = z3.BitVec(f'Instruction/{Instruction._counter}/sii/{id(self)}', 1)
        self.immediate = z3.BitVec(f'Instruction/{Instruction._counter}/imm/{id(self)}', VAL_BITS)
        Instruction._counter += 1

    def get_const(self, current: State, next: State):
        return sum(map(lambda inst: inst.get_const(current, next), self.all_instructions), [])

