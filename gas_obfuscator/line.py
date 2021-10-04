from lark import Lark

with open(dirname(__file__) + '/gas.lark', encoding="utf-8") as g:
    lark_parser = Lark(g.read(), start="exp")

class Line:
    def __init__(self, raw):
        self.raw = raw