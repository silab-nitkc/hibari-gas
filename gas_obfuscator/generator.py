class GASGenerator:
    def __init__(self, operands: list[str], suffix: str):
        self.operands: list[str] = operands
        self.suffix: str = suffix

    def generate_GAS(self, instructions: list[dict]) -> list[str]:
        return list(map(self.generate_code, instructions))

    def generate_code(self, instruction: dict) -> str:
        dst: str = ""
        src: str = ""
        res: str = ""

        if instruction["dst"] is not None:
            dst = self.operands[instruction["dst"]]

        if instruction["src_is_immediate"]:
            src = f'${instruction["immediate"]}'
        elif instruction["src"] is not None:
            src = self.operands[instruction["src"]]

        if instruction["instruction"] in ["add", "sub", "xor", "and", "or", "mov"]:
            res = f"{instruction['instruction']}{self.suffix} {src}, {dst}"

        return res
