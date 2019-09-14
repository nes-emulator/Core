import unittest
from .collection import InstructionCollection
from .instruction import Instruction

class RegisterTest(unittest.TestCase):
    def test_add_absolute_addres(self):
        inst = InstructionCollection.get_instruction(60)
        self.assertEqual(1, inst.get_cycles())
        self.assertEqual(60, inst.opcode)

        result = inst.execute(memory={}, cpu={}, params=[0, 0])
        self.assertEqual(0, result)

    def test_get_instruction_none(self):
        inst = InstructionCollection.get_instruction('inst-non-existent-bla-bla')
        self.assertEqual(1, inst.get_cycles())
        self.assertEqual('none', inst.opcode)