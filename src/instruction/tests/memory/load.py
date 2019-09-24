import unittest
from src.instruction.collection import InstructionCollection
from src.cpu.cpu import CPU
from src.memory.memory import Memory

class LoadTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory()
        # mock state
        self.memory.set_content(100, 77)
        self.memory.set_content(101, 0)
        self.memory.set_content(102, 128)
        self.cpu.state.a.set_value(1)

    def lda_change_a(self):
        opcode = 0xA9
        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[100])

        self.assertEqual(self.cpu.state.a.get_value, 77)

    def lda_change_status(self):
        opcode = 0xA5
        inst = InstructionCollection.get_instruction(opcode)

        # zero
        inst.execute(memory=self.memory, cpu=self.cpu, params=[101])
        self.assertTrue(self.cpu.state.status.zero)
        self.assertFalse(self.cpu.state.status.negative)

        # negative
        inst.execute(memory=self.memory, cpu=self.cpu, params=[102])
        self.assertFalse(self.cpu.state.status.zero)
        self.assertTrue(self.cpu.state.status.negative)
