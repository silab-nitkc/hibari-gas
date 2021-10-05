from __future__ import annotations
from lark import Lark


class Line:
    def __init__(self, raw):
        self.raw = raw
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

    def set_src(self, name: str, has_memory_ref: bool, is_immediate: bool, **other: dict):
        self.src = name
        self.src_has_memory_ref = has_memory_ref
        self.src_is_immediate = is_immediate

        if self.src_is_immediate:
            self.immediate = int(self.src)

    def set_op(self, name: str, tree: list):
        self.op = name
        self.suffix = tree[0]
        self.set_src(**tree[1])
        self.set_dst(**tree[2])

    def is_obfuscatable(self, all_instructions: list[str]):
        if self.op not in all_instructions:
            return False
        return True

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
