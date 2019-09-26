import unittest
from src.instruction.collection import InstructionCollection
from src.cpu.cpu import CPU
from src.memory.memory import Memory


class LsrTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.memory.set_content(100, 8)
        self.memory.set_content(101, 1)

    def test_lsr_accumulator(self):
        self.cpu.state.a.set_value(4)
        opcode = 0x4A
        inst = InstructionCollection.get_instruction(opcode)

        inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        self.assertEqual(self.cpu.state.a.get_value(), 2)
        self.assertFalse(self.cpu.state.status.negative)

    def test_lsr_accumulator_status(self):
        self.cpu.state.a.set_value(1)
        opcode = 0x4A
        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[])

        self.assertEqual(self.cpu.state.a.get_value(), 0)
        self.assertTrue(self.cpu.state.status.zero)
        self.assertTrue(self.cpu.state.status.carry)
        self.assertFalse(self.cpu.state.status.negative)

    def test_lsr(self):
        opcode = 0x46
        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[100])

        self.assertEqual(self.memory.retrieve_content(100), 4)
        self.assertFalse(self.cpu.state.status.negative)

    def test_lsr_status(self):
        opcode = 0x46
        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[101])

        self.assertEqual(self.memory.retrieve_content(101), 0)
        self.assertFalse(self.cpu.state.status.negative)
        self.assertTrue(self.cpu.state.status.zero)
        self.assertTrue(self.cpu.state.status.carry)


class AslTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.memory.set_content(0, 0b10000000)
        self.cpu.state.a.set_value(0b11000000)

    def test_asl_accumulator_flags(self):
        inst = InstructionCollection.get_instruction(0x0A)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        self.assertEqual(self.cpu.state.status.negative, True)
        self.assertEqual(self.cpu.state.status.zero, False)
        self.assertEqual(self.cpu.state.status.carry, True)
        self.assertEqual(self.cpu.state.a.get_value(), 0b10000000)

    def test_asl_memory_ZeroPg_flags(self):
        inst = InstructionCollection.get_instruction(0x06)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[0])
        self.assertEqual(self.cpu.state.status.negative, False)
        self.assertEqual(self.cpu.state.status.zero, True)
        self.assertEqual(self.cpu.state.status.carry, True)
        self.assertEqual(self.memory.retrieve_content(0), 0)
