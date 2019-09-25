import unittest
from src.instruction.collection import InstructionCollection
from src.cpu.cpu import CPU
from src.memory.memory import Memory

class NopTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory()

    def nop_test(self):
        opcode = 0xEA
        inst = InstructionCollection.get_instruction(opcode)
        try:
            inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        # TODO gambiarra
        except:
            assertTrue(False)
