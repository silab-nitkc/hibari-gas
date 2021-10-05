class GASGenerator:
    def __init__(self, operands: list[str]):
        self.operands: list[str] = operands

    def generate_GAS(self, instructions: list[dict]):
        pass

    def generate_code(self, instruction: dict) -> str:
        dst: str = ""
        src: str = ""
        res: str = ""

        if instruction["dst"] is not None:
            dst = self.operands[instruction["dst"]]
        if instruction["src"] is not None:
            if instruction["src_is_immediate"]:
                src = instruction["immediate"]
            else:
                src = self.operands[instruction["src"]]
        if instruction["instruction"] == "add":
            res = f"{instruction['instruction']}{self.suffix} {src}, {dst}"

        return res
