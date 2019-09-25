import unittest
import random

from src.instruction.collection import InstructionCollection
from src.cpu.cpu import CPU
from src.memory.memory import Memory

class TransferTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory()

    def zero_and_negative(self, val):
        if (val == 0):
            self.assertTrue(self.cpu.state.status.zero)
        else:
            self.assertFalse(self.cpu.state.status.zero)

        if (val > 127):
            self.assertTrue(self.cpu.state.status.negative)
        else:
            self.assertFalse(self.cpu.state.status.negative)

        if (val > 0 and val < 127):
            self.assertFalse(self.cpu.state.status.negative)
            self.assertFalse(self.cpu.state.status.zero)

    # given source and destionation registers, test the transfer
    def default_from_to(self, opcode, fromreg, toreg):

        # mock value
        fromreg.set_value(random.randint(0, 255))

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        self.assertEqual(fromreg.get_value(), toreg.get_value())

    # given the source register, test status register
    def default_status(self, opcode, reg):

        reg.set_value(0)
        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        self.zero_and_negative(reg.get_value())

        reg.set_value(128)
        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        self.zero_and_negative(reg.get_value())

        reg.set_value(60)
        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        self.zero_and_negative(reg.get_value())


    def test_tax(self):
        self.default_from_to(0xAA, self.cpu.state.a, self.cpu.state.x)

    def test_tay(self):
        self.default_from_to(0xA8, self.cpu.state.a, self.cpu.state.y)

    def test_tsx(self):
        self.default_from_to(0xBA, self.cpu.state.sp, self.cpu.state.x)

    def test_txa(self):
        self.default_from_to(0x8A, self.cpu.state.x, self.cpu.state.a)

    def test_txs(self):
        self.default_from_to(0x9A, self.cpu.state.x, self.cpu.state.sp)

    def test_tya(self):
        self.default_from_to(0x98, self.cpu.state.y, self.cpu.state.a)

    def test_tax_status(self):
        self.default_status(0xAA, self.cpu.state.a)

    def test_tay_status(self):
        self.default_status(0xA8, self.cpu.state.a)

    def test_tsx_status(self):
        self.default_status(0xBA, self.cpu.state.sp)

    def test_txa_status(self):
        self.default_status(0x8A, self.cpu.state.x)

    def test_tya_status(self):
        self.default_status(0x98, self.cpu.state.y)
