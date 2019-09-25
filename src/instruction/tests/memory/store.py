import unittest
from src.instruction.collection import InstructionCollection
from src.cpu.cpu import CPU
from src.memory.memory import Memory

class StoreTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory()
        # mock state
        self.cpu.state.a.set_value(77)
        self.cpu.state.x.set_value(88)
        self.cpu.state.y.set_value(99)
        self.memory.set_content(100, 55)

    def test_sta_change_mem(self):
        opcode = 0x9D
        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[100])

        self.assertEqual(self.memory.retrieve_content(100), 77)

    def test_stx_change_mem(self):
        opcode = 0x86
        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[100])

        self.assertEqual(self.memory.retrieve_content(100), 88)

    def test_sty_change_mem(self):
        opcode = 0x84
        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[100])

        self.assertEqual(self.memory.retrieve_content(100), 99)
