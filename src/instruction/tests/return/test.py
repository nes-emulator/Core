import unittest
from src.instruction.collection import InstructionCollection
from src.cpu.cpu import CPU
from src.memory.memory import Memory
from src.register.statusregister import StatusRegister


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

    def test_rti(self):
        pc_end = 0xAA01
        status_reg = StatusRegister(0b11110001)
        self.cpu.state.pc.set_value(pc_end)
        self.cpu.state.status = status_reg
        self.memory.stack.push_pc()
        self.memory.stack.push_val(status_reg.to_val())
        self.cpu.state.status.clear()
        self.cpu.state.pc.set_value(0)
        ins = InstructionCollection.get_instruction(0x40)
        ins.execute(self.memory, self.cpu, [])
        self.assertEqual(self.cpu.state.status.to_val(), 0b11110001)
        self.assertEqual(self.cpu.state.pc.get_value(), 0xAA01)
