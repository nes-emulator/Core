import unittest
from src.instruction.collection import InstructionCollection
from src.instruction.instruction import Instruction
from src.cpu.cpu import CPU
from src.memory.memory import Memory

class AddInstructionTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.memory.reset()

    def compare_flags(self, zero, carry, negative, overflow):
        self.assertEqual(zero, self.cpu.state.status.zero)
        self.assertEqual(carry, self.cpu.state.status.carry)
        self.assertEqual(negative, self.cpu.state.status.negative)
        self.assertEqual(overflow, self.cpu.state.status.overflow)

    def test_add_immediate_address_bigger_than_register_size(self):
        opcode = 69
        test_value = 128
        self.cpu.state.a.set_value(test_value)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(0, self.cpu.state.a.get_value())

        self.compare_flags(zero=True, carry=True, negative=False, overflow=True)


    def test_add_immediate_address_negative(self):
        opcode = 69
        test_value = 127
        self.cpu.state.a.set_value(1)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(test_value + 1, self.cpu.state.a.get_value())

        self.compare_flags(zero=False, carry=False, negative=True, overflow=False)

    def test_add_immediate_address_with_carry(self):
        opcode = 69
        test_value = 0
        self.cpu.state.a.set_value(0)
        self.cpu.state.status.carry = True

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(test_value + 1, self.cpu.state.a.get_value())

        self.compare_flags(zero=False, carry=False, negative=False, overflow=False)

    def test_add_immediate_address(self):
        opcode = 69
        test_value = 0

        self.cpu.state.a.set_value(0)

        inst = InstructionCollection.get_instruction(opcode)
        self.assertEqual(1, inst.get_cycles())
        self.assertEqual(opcode, inst.opcode)

        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(test_value, self.cpu.state.a.get_value())

        self.compare_flags(zero=True, carry=False, negative=False, overflow=False)

    def test_add_zero_page_address(self):
        opcode = 65
        test_value = 37
        memory_position = 1

        self.cpu.state.a.set_value(0)
        self.memory.set_content(memory_position, test_value)

        inst = InstructionCollection.get_instruction(opcode)
        self.assertEqual(1, inst.get_cycles())
        self.assertEqual(opcode, inst.opcode)

        inst.execute(memory=self.memory, cpu=self.cpu, params=[memory_position])

        self.assertEqual(test_value, self.memory.retrieve_content(memory_position))
        self.assertEqual(test_value, self.cpu.state.a.get_value())

        self.compare_flags(zero=False, carry=False, negative=False, overflow=False)
