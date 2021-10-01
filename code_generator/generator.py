from .define_instructions import all


class CodeGenerator:
    def __init__(self, instructions=all, instruction_count=5, ):
        self.instructions = all

    def test_generate_add_instruction(self):
        const = []
        inst_seq = InstructionSequence()
        inst_seq.add_instruction(Instruction(all))

        tl1 = Timeline(2)
        const += tl1.get_state(0).set_values([1, 2, 3, 4])
        const += tl1.get_state(1).set_values([1, 2, 7, 4])
        const += tl1.get_const()
        const += inst_seq.instructions[0].get_const(
            tl1.get_state(0), tl1.get_state(1))

        tl2 = Timeline(2)
        const += tl2.get_state(0).set_values([1, 100, 3, 4])
        const += tl2.get_state(1).set_values([1, 100, 7, 4])
        const += tl2.get_const()
        const += inst_seq.instructions[0].get_const(
            tl2.get_state(0), tl2.get_state(1))

        const += get_pc_const(inst_seq.instructions[0])

        sl = z3.Solver()
        sl.add(const)
        sl.check()
        m = sl.model()


if __name__ == "__main__":
    unittest.main()
