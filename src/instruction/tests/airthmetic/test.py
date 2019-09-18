import unittest
from src.instruction.collection import InstructionCollection
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



class IncreaseTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.memory.reset()

    def test_inx_normal(self):
        opcode = 232
        test_value = 67

        self.cpu.state.x.set_value(test_value)
        inst = InstructionCollection.get_instruction(opcode)
        self.assertEqual(opcode, inst.opcode)

        inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        self.assertEqual(test_value + 1, self.cpu.state.x.get_value())
        self.assertEqual(False, self.cpu.state.status.zero)
        self.assertEqual(False, self.cpu.state.status.negative)

    def test_inx_negative(self):
        opcode = 232
        test_value = 127

        self.cpu.state.x.set_value(test_value)
        inst = InstructionCollection.get_instruction(opcode)
        self.assertEqual(opcode, inst.opcode)

        inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        self.assertEqual(test_value + 1, self.cpu.state.x.get_value())
        self.assertEqual(False, self.cpu.state.status.zero)
        self.assertEqual(True, self.cpu.state.status.negative)

    def test_inx_zero(self):
        opcode = 232
        test_value = 255

        self.cpu.state.x.set_value(test_value)
        inst = InstructionCollection.get_instruction(opcode)
        self.assertEqual(opcode, inst.opcode)

        inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        self.assertEqual(0, self.cpu.state.x.get_value())
        self.assertEqual(True, self.cpu.state.status.zero)
        self.assertEqual(False, self.cpu.state.status.negative)

    def test_iny_normal(self):
        opcode = 200
        test_value = 34

        self.cpu.state.y.set_value(test_value)
        inst = InstructionCollection.get_instruction(opcode)
        self.assertEqual(opcode, inst.opcode)

        inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        self.assertEqual(test_value + 1, self.cpu.state.y.get_value())
        self.assertEqual(False, self.cpu.state.status.zero)
        self.assertEqual(False, self.cpu.state.status.negative)

    def test_iny_negative(self):
        opcode = 200
        test_value = 127

        self.cpu.state.y.set_value(test_value)
        inst = InstructionCollection.get_instruction(opcode)
        self.assertEqual(opcode, inst.opcode)

        inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        self.assertEqual(test_value + 1, self.cpu.state.y.get_value())
        self.assertEqual(False, self.cpu.state.status.zero)
        self.assertEqual(True, self.cpu.state.status.negative)

    def test_iny_zero(self):
        opcode = 200
        test_value = 255

        self.cpu.state.y.set_value(test_value)
        inst = InstructionCollection.get_instruction(opcode)
        self.assertEqual(opcode, inst.opcode)

        inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        self.assertEqual(0, self.cpu.state.y.get_value())
        self.assertEqual(True, self.cpu.state.status.zero)
        self.assertEqual(False, self.cpu.state.status.negative)





class DecreaseTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.memory.reset()

    def test_dex_normal(self):
        opcode = 202
        test_value = 67

        self.cpu.state.x.set_value(test_value)
        inst = InstructionCollection.get_instruction(opcode)
        self.assertEqual(opcode, inst.opcode)

        inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        self.assertEqual(test_value - 1, self.cpu.state.x.get_value())
        self.assertEqual(False, self.cpu.state.status.zero)
        self.assertEqual(False, self.cpu.state.status.negative)

    def test_dex_negative(self):
        opcode = 202
        test_value = 0

        self.cpu.state.x.set_value(test_value)
        inst = InstructionCollection.get_instruction(opcode)
        self.assertEqual(opcode, inst.opcode)

        inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        self.assertEqual(255, self.cpu.state.x.get_value())
        self.assertEqual(False, self.cpu.state.status.zero)
        self.assertEqual(True, self.cpu.state.status.negative)

    def test_dex_zero(self):
        opcode = 202
        test_value = 1

        self.cpu.state.x.set_value(test_value)
        inst = InstructionCollection.get_instruction(opcode)
        self.assertEqual(opcode, inst.opcode)

        inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        self.assertEqual(0, self.cpu.state.x.get_value())
        self.assertEqual(True, self.cpu.state.status.zero)
        self.assertEqual(False, self.cpu.state.status.negative)

    def test_dey_normal(self):
        opcode = 136
        test_value = 34

        self.cpu.state.y.set_value(test_value)
        inst = InstructionCollection.get_instruction(opcode)
        self.assertEqual(opcode, inst.opcode)

        inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        self.assertEqual(test_value - 1, self.cpu.state.y.get_value())
        self.assertEqual(False, self.cpu.state.status.zero)
        self.assertEqual(False, self.cpu.state.status.negative)

    def test_dey_negative(self):
        opcode = 136
        test_value = 0

        self.cpu.state.y.set_value(test_value)
        inst = InstructionCollection.get_instruction(opcode)
        self.assertEqual(opcode, inst.opcode)

        inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        self.assertEqual(255, self.cpu.state.y.get_value())
        self.assertEqual(False, self.cpu.state.status.zero)
        self.assertEqual(True, self.cpu.state.status.negative)

    def test_dey_zero(self):
        opcode = 136
        test_value = 1

        self.cpu.state.y.set_value(test_value)
        inst = InstructionCollection.get_instruction(opcode)
        self.assertEqual(opcode, inst.opcode)

        inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        self.assertEqual(0, self.cpu.state.y.get_value())
        self.assertEqual(True, self.cpu.state.status.zero)
        self.assertEqual(False, self.cpu.state.status.negative)



class SubInstructionTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.memory.reset()

    def compare_flags(self, zero, carry, negative, overflow):
        self.assertEqual(zero, self.cpu.state.status.zero)
        self.assertEqual(carry, self.cpu.state.status.carry)
        self.assertEqual(negative, self.cpu.state.status.negative)
        self.assertEqual(overflow, self.cpu.state.status.overflow)

    def test_sub_immediate_address_negative_without_carry(self):
        opcode = 0xE9
        test_value = 127
        self.cpu.state.a.set_value(test_value)

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(255, self.cpu.state.a.get_value())

        self.compare_flags(zero=False, carry=False, negative=True, overflow=True)

    def test_sub_immediate_address_with_carry(self):
        opcode = 0xE9
        sub_value = 3
        test_value = 65

        self.cpu.state.a.set_value(test_value)
        self.cpu.state.status.carry = True

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[sub_value])
        self.assertEqual(test_value - sub_value, self.cpu.state.a.get_value())

        self.compare_flags(zero=False, carry=True, negative=False, overflow=False)

    def test_sub_immediate_address(self):
        opcode = 0xE9
        test_value = 0

        self.cpu.state.a.set_value(test_value)
        self.cpu.state.status.carry = True

        inst = InstructionCollection.get_instruction(opcode)
        self.assertEqual(2, inst.get_cycles())
        self.assertEqual(opcode, inst.opcode)

        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(test_value, self.cpu.state.a.get_value())

        self.compare_flags(zero=True, carry=True, negative=False, overflow=False)
