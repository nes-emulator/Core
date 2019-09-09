import unittest
from .collection import InstructionCollection
from .instruction import Instruction

class RegisterTest(unittest.TestCase):

    def test_get_instruction_add(self):
        inst = InstructionCollection.get_instruction('add')
        self.assertEqual(1, inst.get_cycles())
        self.assertEqual('add', inst.opcode)

        result = inst({})
        self.assertEqual(0, result.a_register)
        self.assertEqual(None, result.x_register)

    def test_get_instruction_sub(self):
        inst = InstructionCollection.get_instruction('sub')
        self.assertEqual(2, inst.get_cycles())
        self.assertEqual('sub', inst.opcode)

        result = inst({})
        self.assertEqual(0, result.x_register)
        self.assertEqual(None, result.a_register)

    def test_get_instruction_none(self):
        inst = InstructionCollection.get_instruction('inst-non-existent-bla-bla')
        self.assertEqual(1, inst.get_cycles())
        self.assertEqual('none', inst.opcode)