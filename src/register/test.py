import unittest
from .register import Register
from .statusregister import StatusRegister

class RegisterTest(unittest.TestCase):

    def test_set_value(self):
        reg = Register(1)
        self.assertEqual(1, reg.get_value())

    def test_status_register_startup(self):
        reg = StatusRegister()
        self.assertEqual(0x34, reg.to_val())