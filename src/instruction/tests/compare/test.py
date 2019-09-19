import unittest
from src.instruction.collection import InstructionCollection
from src.cpu.cpu import CPU
from src.memory.memory import Memory

class CompareInstructionTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.memory.reset()

    def compare_flags(self, zero, carry, negative):
        self.assertEqual(zero, self.cpu.state.status.zero)
        self.assertEqual(carry, self.cpu.state.status.carry)
        self.assertEqual(negative, self.cpu.state.status.negative)

    def test_cpx_compare_equals(self):
        opcode = 0xE0
        test_value = 12

        self.cpu.state.x.set_value(test_value)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.compare_flags(zero=True, carry=True, negative=False)

    def test_cpx_compare_negative(self):
        opcode = 0xE0
        test_value = 34

        self.cpu.state.y.set_value(test_value - 1)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])

        self.compare_flags(zero=False, carry=False, negative=True)

    def test_cpx_compare_carry_only(self):
        opcode = 0xE0
        test_value = 126
        compare_value = 74

        self.cpu.state.x.set_value(test_value)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[compare_value])

        self.compare_flags(zero=False, carry=True, negative=False)

    def test_cpy_compare_equals(self):
        opcode = 0xC0
        test_value = 65

        self.cpu.state.y.set_value(test_value)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.compare_flags(zero=True, carry=True, negative=False)

    def test_cpy_compare_negative(self):
        opcode = 0xC0
        test_value = 72

        self.cpu.state.y.set_value(test_value - 1)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])

        self.compare_flags(zero=False, carry=False, negative=True)

    def test_cpy_compare_carry_only(self):
        opcode = 0xC0
        test_value = 126
        compare_value = 74

        self.cpu.state.y.set_value(test_value)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[compare_value])

        self.compare_flags(zero=False, carry=True, negative=False)

    def test_cmp_compare_equals(self):
        opcode = 0xC9
        test_value = 65

        self.cpu.state.a.set_value(test_value)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.compare_flags(zero=True, carry=True, negative=False)

    def test_cmp_compare_negative(self):
        opcode = 0xC9
        test_value = 72

        self.cpu.state.a.set_value(test_value - 1)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])

        self.compare_flags(zero=False, carry=False, negative=True)

    def test_cmp_compare_carry_only(self):
        opcode = 0xC9
        test_value = 126
        compare_value = 74

        self.cpu.state.a.set_value(test_value)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[compare_value])

        self.compare_flags(zero=False, carry=True, negative=False)


