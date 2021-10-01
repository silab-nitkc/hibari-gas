from abc import ABCMeta, abstractmethod
import z3
from state import State
from instruction import Instruction

REG_BITS = 2

class AbstractInstruction(metaclass = ABCMeta):
    def __init__(self, instruction, current: State, next: State) -> None:
        self.instruction = instruction
        self.current = current
        self.next: State = next
    
    @abstractmethod
    def get_id(self) -> int:
        pass

    @abstractmethod
    def get_const(self) -> list:
        pass
    
    def increment_pc(self) -> list:
        return [self.current.pc + 1 == self.next.pc]
    
    def is_been_called(self):
        return self.instruction.op_id == self.get_id()
    
    def set_zero_flag(self, value: z3.BitVec) -> list:
        return [z3.If(value == 0, self.next.zero_flag == 1, self.next.zero_flag == 0)]
    
    def get_dst(self, state: State, instruction: Instruction):
        return state.values[instruction.dst]
    
    def get_src(self, state: State, instruction: Instruction):
        return z3.If(instruction.src_is_immediate == 0, state.values[instruction.src], instruction.immediate)
    
    def keep_values(self):
        const = []
        inst: Instruction = self.instruction
        for i in range(2 ** REG_BITS):
            const += [z3.If(z3.And(inst.src_is_immediate == 0, inst.dst == i), True, self.get_dst(self.next, inst) == self.get_dst(self.current, inst))]
        return const

all: list[AbstractInstruction] = []

class Add(AbstractInstruction):
    def get_id(self) -> int:
        return 0

    def get_const(self) -> list:
        const: list = []
        
        const += self.increment_pc()

        inst: Instruction = self.instruction
        const += [self.get_dst(self.next, inst) == self.get_dst(self.current, inst) + self.get_src(self.current, inst)]
        const += self.keep_values()

        const += self.set_zero_flag(self.get_dst(self.next, inst))
        
        return [z3.If(self.is_been_called(), z3.And(const), True)]

all += [Add]

def get_pc_const(instruction: Instruction) -> list:
    return [instruction.op_id >= 0, instruction.op_id < len(all)]
