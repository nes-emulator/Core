import unittest
import random

from src.instruction.collection import InstructionCollection
from src.cpu.cpu import CPU
from src.memory.memory import Memory

class TransferTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory()

    def test_zero_and_negative(self, val):
        if (val < 0):
            assertTrue(self.cpu.state.status.zero)
        else:
            assertFalse(self.cpu.state.status.zero)

        if (val > 127):
            assertTrue(self.cpu.state.status.negative)
        else:
            assertFalse(self.cpu.state.status.negative)

    # given source and destionation registers, test the transfer
    def default_from_to(self, opcode, fromreg, toreg):

        # mock value
        fromreg.set_value(random.randint(0, 255))

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        assertEqual(fromreg.get_value(), toreg.get_value())

    # given the source register, test status register
    def default_status(self, opcode, reg):

        reg.set_value(0)
        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        test_zero_and_negative(reg.get_value())

        reg.set_value(128)
        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        test_zero_and_negative(reg.get_value())

        reg.set_value(60)
        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        test_zero_and_negative(reg.get_value())


    def tax_test(self):
        default_from_to(0xAA, self.cpu.state.a, self.cpu.state.x)

    def tay_test(self):
        default_from_to(0xA8, self.cpu.state.a, self.cpu.state.y)

    def tsx_test(self):
        default_from_to(0xBA, self.cpu.state.sp, self.cpu.state.x)

    def txa_test(self):
        default_from_to(0x8A, self.cpu.state.x, self.cpu.state.a)

    def txs_test(self):
        default_from_to(0x9A, self.cpu.state.x, self.cpu.state.sp)

    def tya_test(self):
        default_from_to(0x98, self.cpu.state.y, self.cpu.state.a)

    def tax_status(self):
        default_status(0xAA, self.cpu.state.a)

    def tay_status(self):
        default_status(0xA8, self.cpu.state.a)

    def tsx_status(self):
        default_status(0xBA, self.cpu.state.sp)

    def txa_status(self):
        default_status(0x8A, self.cpu.state.x)

    def tya_status(self):
        default_status(0x98, self.cpu.state.y)
