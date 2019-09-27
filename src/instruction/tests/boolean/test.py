import unittest
from src.instruction.collection import InstructionCollection
from src.cpu.cpu import CPU
from src.memory.memory import Memory


class AndInstructionTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory(self.cpu)
        self.memory.reset()

    def compare_flags(self, zero, carry, negative, overflow):
        self.assertEqual(zero, self.cpu.state.status.zero)
        self.assertEqual(carry, self.cpu.state.status.carry)
        self.assertEqual(negative, self.cpu.state.status.negative)
        self.assertEqual(overflow, self.cpu.state.status.overflow)

    def test_and_immediate_address_zero(self):
        opcode = 0x29
        test_value = 126

        self.cpu.state.a.set_value(1)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(0, self.cpu.state.a.get_value())

        self.compare_flags(zero=True, carry=False, negative=False, overflow=False)

    def test_and_immediate_address_negative(self):
        opcode = 0x29
        test_value = 128

        self.cpu.state.a.set_value(255)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(test_value, self.cpu.state.a.get_value())

        self.compare_flags(zero=False, carry=False, negative=True, overflow=False)

    def test_and_immediate_address(self):
        opcode = 0x29
        test_value = 65

        self.cpu.state.a.set_value(test_value)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(test_value, self.cpu.state.a.get_value())

        self.compare_flags(zero=False, carry=False, negative=False, overflow=False)

    def test_and_zero_page_address(self):
        opcode = 0x25
        test_value = 37
        memory_position = 1

        self.cpu.state.a.set_value(0)
        self.memory.set_content(memory_position, test_value)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[memory_position])
        self.assertEqual(0, self.cpu.state.a.get_value())
        self.assertEqual(test_value, self.memory.retrieve_content(memory_position))

        self.compare_flags(zero=True, carry=False, negative=False, overflow=False)


class EorInstructionTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory(self.cpu)
        self.memory.reset()

    def compare_flags(self, zero, carry, negative, overflow):
        self.assertEqual(zero, self.cpu.state.status.zero)
        self.assertEqual(carry, self.cpu.state.status.carry)
        self.assertEqual(negative, self.cpu.state.status.negative)
        self.assertEqual(overflow, self.cpu.state.status.overflow)

    def test_eor_immediate_address_zero(self):
        opcode = 0x49
        test_value = 126

        self.cpu.state.a.set_value(test_value)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(0, self.cpu.state.a.get_value())

        self.compare_flags(zero=True, carry=False, negative=False, overflow=False)

    def test_eor_immediate_address_negative(self):
        opcode = 0x49
        test_value = 255

        self.cpu.state.a.set_value(127)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(128, self.cpu.state.a.get_value())

        self.compare_flags(zero=False, carry=False, negative=True, overflow=False)

    def test_eor_immediate_address(self):
        opcode = 0x49
        test_value = 126

        self.cpu.state.a.set_value(127)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(1, self.cpu.state.a.get_value())

        self.compare_flags(zero=False, carry=False, negative=False, overflow=False)

    def test_eor_zero_page_address(self):
        opcode = 0x45
        test_value = 98
        memory_position = 166

        self.cpu.state.a.set_value(test_value)
        self.memory.set_content(memory_position, test_value)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[memory_position])
        self.assertEqual(0, self.cpu.state.a.get_value())
        self.assertEqual(test_value, self.memory.retrieve_content(memory_position))

        self.compare_flags(zero=True, carry=False, negative=False, overflow=False)


class OraInstructionTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory(self.cpu)
        self.memory.reset()

    def compare_flags(self, zero, carry, negative, overflow):
        self.assertEqual(zero, self.cpu.state.status.zero)
        self.assertEqual(carry, self.cpu.state.status.carry)
        self.assertEqual(negative, self.cpu.state.status.negative)
        self.assertEqual(overflow, self.cpu.state.status.overflow)

    def test_ora_immediate_address_zero(self):
        opcode = 0x09
        test_value = 0

        self.cpu.state.a.set_value(test_value)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(0, self.cpu.state.a.get_value())

        self.compare_flags(zero=True, carry=False, negative=False, overflow=False)

    def test_ora_immediate_address_negative(self):
        opcode = 0x09
        test_value = 128

        self.cpu.state.a.set_value(0)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(test_value, self.cpu.state.a.get_value())

        self.compare_flags(zero=False, carry=False, negative=True, overflow=False)

    def test_ora_immediate_address(self):
        opcode = 0x09
        test_value = 65

        self.cpu.state.a.set_value(test_value)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(test_value, self.cpu.state.a.get_value())

        self.compare_flags(zero=False, carry=False, negative=False, overflow=False)

    def test_ora_zero_page_address(self):
        opcode = 0x05
        test_value = 37
        memory_position = 1

        self.cpu.state.a.set_value(0)
        self.memory.set_content(memory_position, test_value)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[memory_position])
        self.assertEqual(test_value, self.cpu.state.a.get_value())
        self.assertEqual(test_value, self.memory.retrieve_content(memory_position))

        self.compare_flags(zero=False, carry=False, negative=False, overflow=False)


class BitInstructionTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory(self.cpu)
        self.memory.reset()

    def compare_flags(self, zero, carry, negative, overflow):
        self.assertEqual(zero, self.cpu.state.status.zero)
        self.assertEqual(carry, self.cpu.state.status.carry)
        self.assertEqual(negative, self.cpu.state.status.negative)
        self.assertEqual(overflow, self.cpu.state.status.overflow)

    def test_bit_zero_page_address_zero_flag(self):
        opcode = 0x24
        test_value = 8
        memory_position = 33

        self.cpu.state.a.set_value(7)
        self.memory.set_content(memory_position, test_value)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[memory_position])
        self.assertEqual(7, self.cpu.state.a.get_value())
        self.assertEqual(test_value, self.memory.retrieve_content(memory_position))

        self.compare_flags(zero=True, carry=False, negative=False, overflow=False)

    def test_bit_zero_page_address_negative_flag(self):
        opcode = 0x24
        test_value = 140
        memory_position = 43

        self.cpu.state.a.set_value(128)
        self.memory.set_content(memory_position, test_value)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[memory_position])
        self.assertEqual(128, self.cpu.state.a.get_value())
        self.assertEqual(test_value, self.memory.retrieve_content(memory_position))

        self.compare_flags(zero=False, carry=False, negative=True, overflow=False)

    def test_bit_zero_page_address_overflow_flag(self):
        opcode = 0x24
        test_value = 0x42
        memory_position = 53

        self.cpu.state.a.set_value(10)
        self.memory.set_content(memory_position, test_value)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[memory_position])
        self.assertEqual(10, self.cpu.state.a.get_value())
        self.assertEqual(test_value, self.memory.retrieve_content(memory_position))

        self.compare_flags(zero=False, carry=False, negative=False, overflow=True)

    def test_bit_absolute_address_all_flags(self):
        opcode = 0x2C
        test_value = 254
        memory_position = 0b0000100000001010

        low_byte = 0b1010
        high_byte = 0b1000

        self.cpu.state.a.set_value(1)
        self.memory.set_content(memory_position, test_value)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[low_byte, high_byte])
        self.assertEqual(1, self.cpu.state.a.get_value())
        self.assertEqual(test_value, self.memory.retrieve_content(memory_position))

        self.compare_flags(zero=True, carry=False, negative=True, overflow=True)
