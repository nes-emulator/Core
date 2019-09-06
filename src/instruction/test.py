import unittest
from .mapper import InstructionMapper

class RegisterTest(unittest.TestCase):

    def test_get_instruction(self):
        inst = InstructionMapper.get_instruction(1)
        self.assertEquals(1, inst.get_cycles())