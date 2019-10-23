import unittest
from src.util.util import *


class UtilTests(unittest.TestCase):

    def test_make_16b_binary(self):
        b1 = 0b10000000
        b2 = 0b11111111
        res = make_16b_binary(b1, b2)
        self.assertEqual(0b1000000011111111, res)

    def test_extract_8_bit(self):
        for number in range(256):
            bits = extract_8_bits(number)
            expected_result = int("".join(str(x) for x in bits), 2)
            self.assertEqual(8, len(bits))
            self.assertEqual(number, expected_result)