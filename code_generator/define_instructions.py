from abc import ABCMeta, abstractmethod
import z3
from .state import State
from .instruction import Instruction
from .const import *


class AbstractInstruction(metaclass=ABCMeta):
    def __init__(self, instruction: Instruction) -> None:
        self.instruction = instruction

    @abstractmethod
    def get_id(self) -> int:
        pass

    @abstractmethod
    def get_const(self, current: State, next: State) -> list:
        pass

    def increment_pc(self, current: State, next: State) -> list:
        return [current.pc + 1 == next.pc]

    def is_been_called(self):
        return self.instruction.op_id == self.get_id()

    def set_zero_flag(self, value: z3.BitVec, next: State) -> list:
        return [z3.If(value == 0, next.zero_flag == 1, next.zero_flag == 0)]

    def get_dst(self, state: State):
        return state.values[self.instruction.dst]

    def get_src(self, state: State):
        return z3.If(self.instruction.src_is_immediate == 0, state.values[self.instruction.src], self.instruction.immediate)

    def keep_values(self, current: State, next: State):
        const = []
        inst: Instruction = self.instruction
        for i in range(2 ** REG_BITS):
            const += [z3.If(z3.And(inst.src_is_immediate == 0, inst.dst ==
                            i), True, next.values[i] == current.values[i])]
        return const


all: list[AbstractInstruction] = []


class Add(AbstractInstruction):
    def get_id(self) -> int:
        return 0

    def get_const(self, current: State, next: State) -> list:
        const: list = []

        const += self.increment_pc(current, next)

        const += [self.get_dst(next) ==
                  self.get_dst(current) + self.get_src(current)]
        const += self.keep_values(current, next)

        const += self.set_zero_flag(self.get_dst(next), next)

        return [z3.If(self.is_been_called(), z3.And(const), True)]

all += [Add]

class Sub(AbstractInstruction):
    def get_id(self) -> int:
        return 1

    def get_const(self, current: State, next: State) -> list:
        const: list = []

        const += self.increment_pc(current, next)

        const += [self.get_dst(next) ==
                  self.get_dst(current) - self.get_src(current)]
        const += self.keep_values(current, next)

        const += self.set_zero_flag(self.get_dst(next), next)

        return [z3.If(self.is_been_called(), z3.And(const), True)]

all += [Sub]

class Xor(AbstractInstruction):
    def get_id(self) -> int:
        return 2

    def get_const(self, current: State, next: State) -> list:
        const: list = []

        const += self.increment_pc(current, next)

        const += [self.get_dst(next) ==
                  self.get_dst(current) ^ self.get_src(current)]
        const += self.keep_values(current, next)

        const += self.set_zero_flag(self.get_dst(next), next)

        return [z3.If(self.is_been_called(), z3.And(const), True)]

all += [Xor]

class Or(AbstractInstruction):
    def get_id(self) -> int:
        return 3

    def get_const(self, current: State, next: State) -> list:
        const: list = []

        const += self.increment_pc(current, next)

        const += [self.get_dst(next) ==
                  self.get_dst(current) | self.get_src(current)]
        const += self.keep_values(current, next)

        const += self.set_zero_flag(self.get_dst(next), next)

        return [z3.If(self.is_been_called(), z3.And(const), True)]

all += [Or]

class And(AbstractInstruction):
    def get_id(self) -> int:
        return 4

    def get_const(self, current: State, next: State) -> list:
        const: list = []

        const += self.increment_pc(current, next)

        const += [self.get_dst(next) ==
                  self.get_dst(current) & self.get_src(current)]
        const += self.keep_values(current, next)

        const += self.set_zero_flag(self.get_dst(next), next)

        return [z3.If(self.is_been_called(), z3.And(const), True)]

all += [And]

class Mov(AbstractInstruction):
    def get_id(self) -> int:
        return 5

    def get_const(self, current: State, next: State) -> list:
        const: list = []

        const += self.increment_pc(current, next)

        const += [self.get_dst(next) == self.get_src(current)]
        const += self.keep_values(current, next)

        const += [next.zero_flag == current.zero_flag]

        return [z3.If(self.is_been_called(), z3.And(const), True)]

all += [Mov]

def get_pc_const(instruction: Instruction) -> list:
    return [instruction.op_id >= 0, instruction.op_id < len(all)]
