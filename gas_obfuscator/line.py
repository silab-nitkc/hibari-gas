from __future__ import annotations


class Line:
    def __init__(self, raw: str):
        self.raw: str = raw
        self.op = None
        self.suffix = None

        self.dst: str = None
        self.dst_has_memory_ref: bool = None

        self.src = None
        self.src_has_memory_ref: bool = None
        self.src_is_immediate: bool = None

        self.immediate = None
        self.label = None

    def set_dst(self, name: str, has_memory_ref: bool, **other: dict):
        self.dst = name
        self.dst_has_memory_ref = has_memory_ref

    def set_src(self, name: str, has_memory_ref: bool, is_immediate: bool, immediate: int, **other: dict):
        self.src = name
        self.src_has_memory_ref = has_memory_ref
        self.src_is_immediate = is_immediate

        if self.src_is_immediate:
            self.immediate = immediate

    def set_op(self, name: str, tree: list):
        self.op = name
        self.suffix = tree[0]
        self.set_src(**tree[1])
        self.set_dst(**tree[2])

    def is_obfuscatable(self, all_instructions: list[str]):
        if self.op not in all_instructions:
            return False
        return True

    def update_raw(self) -> None:
        if self.op in ["add", "sub", "xor", "or", "and", "mov"]:
            if self.src_is_immediate:
                self.raw = f'{self.op}{self.suffix} ${self.immediate}, {self.dst}'
                return
            else:
                self.raw = f'{self.op}{self.suffix} {self.src}, {self.dst}'
                return

    @staticmethod
    def get_operands(lines: list[__class__]) -> dict:
        res: dict = {}
        for line in lines:
            # None（未設定）もありえるので is False を使う

            if line.src_is_immediate is False:
                res[line.src] = None

            if line.dst is not None:
                res[line.dst] = None

            if line.label is not None:
                res[line.label] = None

        return res

    @staticmethod
    def _convert_to_line(instruction: dict, operands: list[str], suffix: str) -> __class__:
        res: __class__ = Line("")
        temp: list = [
            suffix,
            {
                "name": operands[instruction["src"]] if instruction["src"] is not None else None,
                "has_memory_ref": None,
                "is_immediate": instruction["src_is_immediate"] == 1,
                "immediate": instruction["immediate"]
            },
            {
                "name": operands[instruction["dst"]],

                "has_memory_ref": None,

            }
        ]
        res.set_op(instruction["instruction"], temp)
        res.update_raw()
        return res

    @staticmethod
    def convert_to_lines(instructions: list[dict], operands: list[str], suffix: str) -> list[__class__]:
        return [Line._convert_to_line(i, operands, suffix) for i in instructions]

    @staticmethod
    def get_operands_with_memory_ref(lines: list[__class__]) -> dict:
        operands = Line.get_operands(lines)
        for line in lines:
            if line.src in operands:
                operands[line.src] = line.src_has_memory_ref
            if line.dst in operands:
                operands[line.dst] = line.dst_has_memory_ref
        return operands
