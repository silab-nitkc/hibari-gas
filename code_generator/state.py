import z3
from .const import *
from random import randint


class State:
    _counter = 0

    def __init__(self) -> None:
        self.values = z3.Array(
            f'State/{State._counter}/values', z3.BitVecSort(REG_BITS), z3.BitVecSort(VAL_BITS))
        self.pc = z3.BitVec(f'State/{State._counter}/pc', PC_BITS)
        self.zero_flag = z3.BitVec(f'State/{State._counter}/zero_flag', 2)
        State._counter += 1

    def set_values(self, values: list[int], randomize: bool = False):
        res: list = []
        for value, init in zip(self.values, values):
            if init is None:
                if randomize:
                    res += [value == randint(0, 255)]
            else:
                res += [value == init]

        return res
