import unittest
from src.instruction.collection import InstructionCollection
from src.cpu.cpu import CPU
from src.memory.cpu.memory import Memory


class LoadTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory(self.cpu)
        # mock state
        self.memory.set_content(100, 77)
        self.memory.set_content(101, 0)
        self.memory.set_content(102, 128)
        self.cpu.state.a.set_value(1)
        self.cpu.state.x.set_value(1)
        self.cpu.state.y.set_value(1)

    def test_lda_change_a(self):
        opcode = 0xAD
        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[0x64, 0x00])

        self.assertEqual(self.cpu.state.a.get_value(), 77)

    def test_lda_change_a_immediate(self):
        opcode = 0xA9
        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[77])

        self.assertEqual(self.cpu.state.a.get_value(), 77)

    def test_lda_change_status(self):
        opcode = 0xAD
        inst = InstructionCollection.get_instruction(opcode)

        # zero
        inst.execute(memory=self.memory, cpu=self.cpu, params=[0x65, 0x00])
        self.assertTrue(self.cpu.state.status.zero)
        self.assertFalse(self.cpu.state.status.negative)

        # negative
        inst.execute(memory=self.memory, cpu=self.cpu, params=[0x66, 0x00])
        self.assertFalse(self.cpu.state.status.zero)
        self.assertTrue(self.cpu.state.status.negative)

    def test_ldx_change_x(self):
        opcode = 0xAE
        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[0x64, 0x00])

        self.assertEqual(self.cpu.state.x.get_value(), 77)

    def test_ldx_change_x_immediate(self):
        opcode = 0xA2
        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[77])

        self.assertEqual(self.cpu.state.x.get_value(), 77)

    def test_ldx_change_status(self):
        opcode = 0xAE
        inst = InstructionCollection.get_instruction(opcode)

        # zero
        inst.execute(memory=self.memory, cpu=self.cpu, params=[0x65, 0x00])
        self.assertTrue(self.cpu.state.status.zero)
        self.assertFalse(self.cpu.state.status.negative)

        # negative
        inst.execute(memory=self.memory, cpu=self.cpu, params=[0x66, 0x00])
        self.assertFalse(self.cpu.state.status.zero)
        self.assertTrue(self.cpu.state.status.negative)

    def test_ldy_change_y(self):
        opcode = 0xAC
        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[0x64, 0x00])

        self.assertEqual(self.cpu.state.y.get_value(), 77)

    def test_ldy_change_status(self):
        opcode = 0xAC
        inst = InstructionCollection.get_instruction(opcode)

        # zero
        inst.execute(memory=self.memory, cpu=self.cpu, params=[0x65, 0x00])
        self.assertTrue(self.cpu.state.status.zero)
        self.assertFalse(self.cpu.state.status.negative)

        # negative
        inst.execute(memory=self.memory, cpu=self.cpu, params=[0x66, 0x00])
        self.assertFalse(self.cpu.state.status.zero)
        self.assertTrue(self.cpu.state.status.negative)


class StoreTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory(self.cpu)
        # mock state
        self.cpu.state.a.set_value(77)
        self.cpu.state.x.set_value(88)
        self.cpu.state.y.set_value(99)
        self.memory.set_content(100, 55)

    def test_sta_change_mem(self):
        opcode = 0x85
        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[100])

        self.assertEqual(self.memory.retrieve_content(100), 77)

    def test_stx_change_mem(self):
        opcode = 0x86
        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[100])

        self.assertEqual(self.memory.retrieve_content(100), 88)

    def test_sty_change_mem(self):
        opcode = 0x84
        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[100])

        self.assertEqual(self.memory.retrieve_content(100), 99)


class StackInstTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory(self.cpu)
        self.top = self.memory.stack.get_top()

    def test_pha(self):
        self.cpu.state.a.set_value(0xA)
        opcode = 0x48
        inst = InstructionCollection.get_instruction(opcode)
        addr = inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        self.assertEqual(addr, self.top)
        self.assertEqual(self.memory.stack.get_top(), self.top - 1)
        self.assertEqual(0xA, self.memory.retrieve_content(self.top))

    def test_pla(self):
        self.cpu.state.a.set_value(0xA)
        self.cpu.state.a.set_value(0)
        self.test_pha()
        opcode = 0x68
        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[])
        self.assertEqual(self.memory.stack.get_top(), self.top)
        self.assertEqual(0xA, self.cpu.state.a.get_value())

    # def test_php(self):
    #     sts = StatusRegister(0b10101010)
    #     self.cpu.state.status = sts
    #     opcode = 0x8
    #     inst = InstructionCollection.get_instruction(opcode)
    #     addr = inst.execute(memory=self.memory, cpu=self.cpu, params=[])
    #     self.assertEqual(addr, self.top)
    #     self.assertEqual(self.memory.stack.get_top(), self.top - 1)
    #     self.assertEqual(0b10101010, self.memory.retrieve_content(self.top))
    #
    # def test_plp(self):
    #     self.test_php()
    #     self.cpu.state.status.clear()
    #     opcode = 0x28
    #     inst = InstructionCollection.get_instruction(opcode)
    #     inst.execute(memory=self.memory, cpu=self.cpu, params=[])
    #     self.assertEqual(self.memory.stack.get_top(), self.top)
    #     self.assertEqual(self.cpu.state.status.to_val(), 0b10101010)
