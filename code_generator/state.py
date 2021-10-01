import z3
from .const import *


class State:
    _counter = 0

    def __init__(self) -> None:
        self.values = z3.Array(
            f'State/{State._counter}/values', z3.BitVecSort(REG_BITS), z3.BitVecSort(VAL_BITS))
        self.pc = z3.BitVec(f'State/{State._counter}/pc', PC_BITS)
        self.zero_flag = z3.BitVec(f'State/{State._counter}/zero_flag', 2)
        State._counter += 1

    def set_values(self, values: list[int]):
        return list(map(lambda val: val[0] == val[1], zip(self.values, values)))
