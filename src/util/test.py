import unittest
from src.util.util import *


class UtilTests(unittest.TestCase):

    def test_make_16b_binary(self):
        b1 = 0b10000000
        b2 = 0b11111111
        res = make_16b_binary(b1, b2)
        self.assertEqual(0b1000000011111111, res)
