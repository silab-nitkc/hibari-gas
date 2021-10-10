import unittest
import sys
import os
from lark import Lark
import os
import sys

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from gas_obfuscator import *  # noqa


class TestGASSimulator(unittest.TestCase):
    def test_IO_add(self):
        target: list[Line] = [parse(r"addq $12, %rax")]

        simulator: Simulator = Simulator(target)
        res: dict
        _, res = simulator.run({
            r"%rax": 123,
        })
        expected: dict = {
            r"%rax": 135,
        }
        self.assertEqual(res, expected)

    def test_IO_sub(self):
        target: list[Line] = [parse(r"subq $12, %rax")]

        simulator: Simulator = Simulator(target)
        res: dict
        _, res = simulator.run({
            r"%rax": 123,
        })
        expected: dict = {
            r"%rax": 111,
        }
        self.assertEqual(res, expected)

    def test_IO_xor(self):
        target: list[Line] = [parse(r"xorq $12, %rax")]

        simulator: Simulator = Simulator(target)
        res: dict
        _, res = simulator.run({
            r"%rax": 123,
        })
        expected: dict = {
            r"%rax": 119,
        }
        self.assertEqual(res, expected)

    def test_IO_and(self):
        target: list[Line] = [parse(r"andq $12, %rax")]

        simulator: Simulator = Simulator(target)
        res: dict
        _, res = simulator.run({
            r"%rax": 123,
        })
        expected: dict = {
            r"%rax": 8,
        }
        self.assertEqual(res, expected)

    def test_IO_or(self):
        target: list[Line] = [parse(r"orq $12, %rax")]

        simulator: Simulator = Simulator(target)
        _, res = simulator.run({
            r"%rax": 123,
        })
        expected: dict = {
            r"%rax": 127,
        }
        self.assertEqual(res, expected)

    def test_IO_mov(self):
        target: list[Line] = [parse(r"movq $12, %rax")]

        simulator: Simulator = Simulator(target)
        res: dict
        _, res = simulator.run({
            r"%rax": 123,
        })
        expected: dict = {
            r"%rax": 12,
        }
        self.assertEqual(res, expected)


if __name__ == "__main__":
    unittest.main()
