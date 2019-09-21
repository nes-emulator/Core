import unittest
from src.instruction.collection import InstructionCollection
from src.cpu.cpu import CPU
from src.memory.memory import Memory

class BranchInstructionTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.memory.reset()

        self.cpu.state.pc.set_value(10)

    def test_bcc_changing_pc(self):
        opcode = 0x90
        old_value = self.cpu.state.pc.get_value()
        test_value = 124

        self.cpu.state.status.carry = False

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(old_value + test_value, self.cpu.state.pc.get_value())

    def test_bcc_maintaining_pc(self):
        opcode = 0x90
        old_value = self.cpu.state.pc.get_value()
        test_value = 124

        self.cpu.state.status.carry = True

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(old_value, self.cpu.state.pc.get_value())

    def test_bcs_changing_pc(self):
        opcode = 0xB0
        old_value = self.cpu.state.pc.get_value()
        test_value = 124

        self.cpu.state.status.carry = True

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(old_value + test_value, self.cpu.state.pc.get_value())

    def test_bcs_maintaining_pc(self):
        opcode = 0xB0
        old_value = self.cpu.state.pc.get_value()
        test_value = 124

        self.cpu.state.status.carry = False

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(old_value, self.cpu.state.pc.get_value())

    def test_beq_changing_pc(self):
        opcode = 0xF0
        old_value = self.cpu.state.pc.get_value()
        test_value = 124

        self.cpu.state.status.zero = True

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(old_value + test_value, self.cpu.state.pc.get_value())

    def test_beq_maintaining_pc(self):
        opcode = 0xF0
        old_value = self.cpu.state.pc.get_value()
        test_value = 124

        self.cpu.state.status.zero = False

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(old_value, self.cpu.state.pc.get_value())

    def test_bne_changing_pc(self):
        opcode = 0xD0
        old_value = self.cpu.state.pc.get_value()
        test_value = 124

        self.cpu.state.status.zero = False

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(old_value + test_value, self.cpu.state.pc.get_value())

    def test_bne_maintaining_pc(self):
        opcode = 0xD0
        old_value = self.cpu.state.pc.get_value()
        test_value = 124

        self.cpu.state.status.zero = True

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(old_value, self.cpu.state.pc.get_value())

    def test_bmi_changing_pc(self):
        opcode = 0x30
        old_value = self.cpu.state.pc.get_value()
        test_value = 124

        self.cpu.state.status.negative = True

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(old_value + test_value, self.cpu.state.pc.get_value())

    def test_bmi_maintaining_pc(self):
        opcode = 0x30
        old_value = self.cpu.state.pc.get_value()
        test_value = 124

        self.cpu.state.status.negative = False

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(old_value, self.cpu.state.pc.get_value())

    def test_bpl_changing_pc(self):
        opcode = 0x10
        old_value = self.cpu.state.pc.get_value()
        test_value = 124

        self.cpu.state.status.negative = False

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(old_value + test_value, self.cpu.state.pc.get_value())

    def test_bpl_maintaining_pc(self):
        opcode = 0x10
        old_value = self.cpu.state.pc.get_value()
        test_value = 124

        self.cpu.state.status.negative = True

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(old_value, self.cpu.state.pc.get_value())

    def test_bvc_changing_pc(self):
        opcode = 0x50
        old_value = self.cpu.state.pc.get_value()
        test_value = 124

        self.cpu.state.status.overflow = False

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(old_value + test_value, self.cpu.state.pc.get_value())

    def test_bvc_maintaining_pc(self):
        opcode = 0x50
        old_value = self.cpu.state.pc.get_value()
        test_value = 124

        self.cpu.state.status.overflow = True

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(old_value, self.cpu.state.pc.get_value())

    def test_bvs_changing_pc(self):
        opcode = 0x70
        old_value = self.cpu.state.pc.get_value()
        test_value = 124

        self.cpu.state.status.overflow = True

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(old_value + test_value, self.cpu.state.pc.get_value())

    def test_bvs_maintaining_pc(self):
        opcode = 0x70
        old_value = self.cpu.state.pc.get_value()
        test_value = 124

        self.cpu.state.status.overflow = False

        inst = InstructionCollection.get_instruction(opcode)
        inst.execute(memory=self.memory, cpu=self.cpu, params=[test_value])
        self.assertEqual(old_value, self.cpu.state.pc.get_value())