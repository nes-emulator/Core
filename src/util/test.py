import unittest
from src.util.util import *


class UtilTests(unittest.TestCase):

    def test_make_16b_binary(self):
        b1 = 0b10000000
        b2 = 0b11111111
        res = make_16b_binary(b1, b2)
        self.assertEqual(0b1000000011111111, res)

    def test_add_binary(self):
        b1 = 0b01011  # 11, length = 5
        b2 = 0b00000001  # 1, length = 8
        res, c = add_binary(b1, b2, 8)
        self.assertEqual(res, 12)
        self.assertEqual(c, 0)

    def test_add_binary_carry(self):
        b1 = 0b111  # 11, length = 5
        b2 = 0b1111  # 1, length = 8
        res, c = add_binary(b1, b2, 8)
        self.assertEqual(res, 0b110)
        self.assertEqual(c, 1)
