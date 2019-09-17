import unittest
from src.instruction.collection import InstructionCollection
from src.instruction.instruction import Instruction

class InstructionTest(unittest.TestCase):
    def test_get_instruction_none(self):
        inst = InstructionCollection.get_instruction('inst-non-existent-bla-bla')
        self.assertEqual(1, inst.get_cycles())
        self.assertEqual('none', inst.opcode)