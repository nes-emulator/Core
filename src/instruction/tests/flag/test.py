import unittest
from src.instruction.collection import InstructionCollection
from src.instruction.instruction import Instruction
from src.cpu.cpu import CPU
from src.memory.memory import Memory

class FlagInstructionTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.memory.reset()

    def test_clc(self):
        opcode = 24
        self.cpu.state.status.carry = True

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[])

        self.assertEqual(opcode, inst.opcode)
        self.assertEqual(False, self.cpu.state.status.carry)

    def test_sec(self):
        opcode = 56
        self.cpu.state.status.carry = False

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[])

        self.assertEqual(opcode, inst.opcode)
        self.assertEqual(True, self.cpu.state.status.carry)

    def test_cli(self):
        opcode = 88
        self.cpu.state.status.interrupt = True

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[])

        self.assertEqual(opcode, inst.opcode)
        self.assertEqual(False, self.cpu.state.status.interrupt)

    def test_sei(self):
        opcode = 120
        self.cpu.state.status.interrupt = False

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[])

        self.assertEqual(opcode, inst.opcode)
        self.assertEqual(True, self.cpu.state.status.interrupt)

    def test_clv(self):
        opcode = 184
        self.cpu.state.status.overflow = True

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[])

        self.assertEqual(opcode, inst.opcode)
        self.assertEqual(False, self.cpu.state.status.overflow)

    def test_cld(self):
        opcode = 216
        self.cpu.state.status.decimal = True

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[])

        self.assertEqual(opcode, inst.opcode)
        self.assertEqual(False, self.cpu.state.status.decimal)

    def test_sed(self):
        opcode = 248
        self.cpu.state.status.decimal = False

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[])

        self.assertEqual(opcode, inst.opcode)
        self.assertEqual(True, self.cpu.state.status.decimal)

    def test_brk(self):
        opcode = 0
        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[])

        self.assertEqual(opcode, inst.opcode)
        self.assertEqual(True, self.cpu.state.status.brk)