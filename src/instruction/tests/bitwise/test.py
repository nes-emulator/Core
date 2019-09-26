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
        ret = inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        self.assertEqual(self.cpu.state.status.negative, True)
        self.assertEqual(self.cpu.state.status.zero, False)
        self.assertEqual(self.cpu.state.status.carry, True)
        self.assertEqual(self.cpu.state.a.get_value(), 0b10000000)
        self.assertEqual(ret, None)

    def test_asl_memory_ZeroPg_flags(self):
        inst = InstructionCollection.get_instruction(0x06)
        addr = inst.execute(memory=self.memory, cpu=self.cpu, params=[0])
        self.assertEqual(self.cpu.state.status.negative, False)
        self.assertEqual(self.cpu.state.status.zero, True)
        self.assertEqual(self.cpu.state.status.carry, True)
        self.assertEqual(self.memory.retrieve_content(0), 0)
        self.assertEqual(addr, 0)


class RolTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.memory.set_content(0xA000, 0b11000000)
        self.cpu.state.a.set_value(0b01000000)

    def test_rol_accumulator_flags(self):
        self.cpu.state.status.carry = True
        inst = InstructionCollection.get_instruction(0x2A)
        ret = inst.execute(self.memory, self.cpu, [])
        self.assertEqual(self.cpu.state.a.get_value(), 0b10000001)
        self.assertEqual(self.cpu.state.status.negative, True)
        self.assertEqual(self.cpu.state.status.zero, False)
        self.assertEqual(self.cpu.state.status.carry, False)
        self.assertEqual(ret, None)

    def test_rol_abs_flags(self):
        params = [0, 0xA0]
        self.cpu.state.status.carry = False
        inst = InstructionCollection.get_instruction(0x2E)
        ret = inst.execute(self.memory, self.cpu, params)
        self.assertEqual(0xA000, ret)
        self.assertEqual(self.memory.retrieve_content(0XA000), 0b10000000)
        self.assertEqual(self.cpu.state.status.negative, True)
        self.assertEqual(self.cpu.state.status.zero, False)
        self.assertEqual(self.cpu.state.status.carry, True)


class RorTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.memory.set_content(0xA000, 0b0000000011)
        self.cpu.state.a.set_value(0b00000010)

    def test_ror_accumulator_flags(self):
        self.cpu.state.status.carry = True
        inst = InstructionCollection.get_instruction(0x6A)
        ret = inst.execute(self.memory, self.cpu, [])
        self.assertEqual(self.cpu.state.a.get_value(), 0b10000001)
        self.assertEqual(self.cpu.state.status.negative, True)
        self.assertEqual(self.cpu.state.status.zero, False)
        self.assertEqual(self.cpu.state.status.carry, False)
        self.assertEqual(ret, None)

    def test_ror_abs_flags(self):
        params = [0, 0xA0]
        self.cpu.state.status.carry = False
        inst = InstructionCollection.get_instruction(0x6E)
        ret = inst.execute(self.memory, self.cpu, params)
        self.assertEqual(0xA000, ret)
        self.assertEqual(self.memory.retrieve_content(0XA000), 0b00000001)
        self.assertEqual(self.cpu.state.status.negative, False)
        self.assertEqual(self.cpu.state.status.zero, False)
        self.assertEqual(self.cpu.state.status.carry, True)
