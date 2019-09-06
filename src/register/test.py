import unittest
from .register import Register

class RegisterTest(unittest.TestCase):

    def test_set_value(self):
        reg = Register(1)
        self.assertEqual(1, reg.get_value())