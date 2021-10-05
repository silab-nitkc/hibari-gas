import unittest
import sys
import os
from lark import Lark
import os
import sys

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from gas_obfuscator import *  # noqa


class TestGASObfuscator(unittest.TestCase):
    def test_initialize(self):
        target: str = """
            dummy: .space 160

            addq $12, %rax
        """

        obfuscator: Obfuscator = Obfuscator(target)

    def test_initialize(self):
        target: str = """
            dummy: .space 160

            addq $12, %rax
            subq $12, %rax
            test hoge
            movq $12, %rax
        """

        obfuscator: Obfuscator = Obfuscator(target, ["add", "sub"])
        print(obfuscator.run(2))


if __name__ == "__main__":
    unittest.main()
