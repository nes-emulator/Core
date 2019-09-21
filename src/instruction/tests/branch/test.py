import unittest
from src.instruction.collection import InstructionCollection
from src.cpu.cpu import CPU
from src.memory.memory import Memory

class BranchInstructionTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.memory.reset()

        self.cpu.state.pc.set_value(10)

    def test_bcc_changing_pc(self):
        opcode = 0x90
        old_value = self.cpu.state.pc.get_value()
        test_value = 124

        self.cpu.state.status.carry = False

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(old_value + test_value, self.cpu.state.pc.get_value())

    def test_bcc_maintaining_pc(self):
        opcode = 0x90
        old_value = self.cpu.state.pc.get_value()
        test_value = 124

        self.cpu.state.status.carry = True

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(old_value, self.cpu.state.pc.get_value())