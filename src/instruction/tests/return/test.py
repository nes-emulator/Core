import unittest
from src.instruction.collection import InstructionCollection
from src.cpu.cpu import CPU
from src.memory.memory import Memory


class ReturnTests(unittest.TestCase):

    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory(self.cpu)

    def test_rts(self):
        pc_end = 0xAA01
        top = self.memory.stack.get_top()
        # + 1 = 0xAA 02
        self.cpu.state.pc.set_value(pc_end)
        self.memory.stack.push_pc()
        self.cpu.state.pc.set_value(0)
        ins = InstructionCollection.get_instruction(0x60)
        ins.execute(self.memory, self.cpu, [])
        self.assertEqual(self.cpu.state.pc.get_value(), 0xAA02)
        self.assertEqual(top, self.memory.stack.get_top())
