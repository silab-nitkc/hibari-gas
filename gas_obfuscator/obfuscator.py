from .parser import parse, Parser
from .line import Line


class Obfuscator:
    def __init__(self, raw: str):
        self.raw: str = raw
        self.lines: List[Line] = list(map(parse, raw.split("\n")))
