from lark import Lark


class Line:
    def __init__(self, raw):
        self.raw = raw
        self.op = None

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

