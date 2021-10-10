import z3
from .state import State
from .instruction import Instruction


class InstructionSequence:
    def __init__(self) -> None:
        self.instructions: list[Instruction] = []

    def add_instruction(self, instruction: Instruction) -> None:
        self.instructions += [instruction]

    def length(self) -> int:
        return len(self.instructions)
