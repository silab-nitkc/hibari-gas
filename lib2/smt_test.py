from timeline import Timeline
import unittest
from instruction import Instruction
from instruction_sequence import InstructionSequence
from instruction_const import all, get_pc_const
import z3


class TestInstructionSequenceGenerator(unittest.TestCase):
    def test_generate_add_instruction(self):
        const = []
        inst_seq = InstructionSequence()

        tl1 = Timeline(2)
        inst_seq.add_instruction(Instruction(
            all, tl1.get_state(0), tl1.get_state(1)))
        const += tl1.get_state(0).set_values([1, 2, 3])
        const += tl1.get_state(1).set_values([1, 5, 3])

        tl2 = Timeline(2)
        inst_seq.add_instruction(Instruction(
            all, tl2.get_state(0), tl2.get_state(1)))
        const += tl2.get_state(0).set_values([1, 2, 3])
        const += tl2.get_state(1).set_values([1, 5, 3])

        const += inst_seq.instructions[0].get_const()
        const += get_pc_const(inst_seq.instructions[0])
        const += tl.get_const()
        print(const)

        sl = z3.Solver()
        sl.add(const)
        sl.check()
        m = sl.model()
        print(m)

if __name__ == "__main__":
    unittest.main()
