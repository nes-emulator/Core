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

    def test_add_immediate_address(self):
        opcode = 69
        test_value = 0

        self.cpu.state.a.set_value(0)

        inst = InstructionCollection.get_instruction(opcode)
        self.assertEqual(1, inst.get_cycles())
        self.assertEqual(opcode, inst.opcode)

        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(test_value, self.cpu.state.a.get_value())

        self.assertEqual(True, self.cpu.state.status.zero)
        self.assertEqual(False, self.cpu.state.status.carry)
        self.assertEqual(False, self.cpu.state.status.negative)
        self.assertEqual(False, self.cpu.state.status.overflow)

    def test_add_absolute_address(self):
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

        self.assertEqual(False, self.cpu.state.status.zero)
        self.assertEqual(False, self.cpu.state.status.carry)
        self.assertEqual(False, self.cpu.state.status.negative)
        self.assertEqual(False, self.cpu.state.status.overflow)