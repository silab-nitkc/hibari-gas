import unittest
import sys
import os
from lark import Lark
import os, sys

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from gas_obfuscator import *  # nopep

class TestGASObfuscator(unittest.TestCase):
    def test_initialize(self):
        target: str = """
            dummy: .space 160

            addq $12, %rax
        """

        obfuscator: Obfuscator = Obfuscator(target)
        
if __name__ == "__main__":
    unittest.main()
