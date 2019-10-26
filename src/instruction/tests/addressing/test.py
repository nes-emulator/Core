import unittest
from src.instruction.addressing.addressing import *
from src.cpu.cpu import CPU
from src.memory.cpu.memory import Memory


class InstructionAddressingTest(unittest.TestCase):
    POSITION_PLACEHOLDER = 1

    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory(self.cpu)
        # memory Mock
        self.memory.memory = [InstructionAddressingTest.POSITION_PLACEHOLDER] * Memory.MEMORY_LIMIT

    def test_ImmediateAddr(self):
        # 1 byte limit
        immediate = 0b1010
        processed_param = ImmediateAddr.calculate_unified_parameter([immediate], self.cpu, self.memory)
        self.assertEqual(processed_param, immediate)

    def test_ZeroPageAddr(self):
        # 1 byte
        zero_pg_addr = 0b1010
        processed_param = ZeroPageAddr.calculate_unified_parameter([zero_pg_addr], self.cpu, self.memory)
        self.assertEqual(processed_param, zero_pg_addr)
        self.assertEqual(self.memory.retrieve_content(processed_param), InstructionAddressingTest.POSITION_PLACEHOLDER)

    def test_AbsoluteAddr(self):
        # 2 bytes
        low_byte = 0b1010
        high_byte = 0b1010
        processed_param = AbsoluteAddr.calculate_unified_parameter([low_byte, high_byte], self.cpu, self.memory)
        self.assertEqual(processed_param, 0b0000101000001010)
        self.assertEqual(self.memory.retrieve_content(processed_param), InstructionAddressingTest.POSITION_PLACEHOLDER)

    def test_ImpliedAddr(self):
        self.assertEqual(ImpliedAddr.parameter_length, 0)

    def test_AccumulatorAddr(self):
        self.cpu.state.a.set_value(0b1010)
        accum = AccumulatorAddr.calculate_unified_parameter([], self.cpu, self.memory)
        self.assertEqual(0b1010, accum)

    def test_ZeroPgDirectIndexedRegXAddr(self):
        self.cpu.state.x.set_value(10)
        zero_pg = 10
        self.memory.set_content(20, 20)
        unified_param = ZeroPgDirectIndexedRegXAddr.calculate_unified_parameter([zero_pg], self.cpu, self.memory)
        self.assertEqual(unified_param, 20)
        self.assertEqual(self.memory.retrieve_content(unified_param), 20)

    def tets_ZeroPgDirectIndexedRegYAddr(self):
        self.cpu.state.y.set_value(10)
        zero_pg = 10
        self.memory.set_content(20, 20)
        unified_param = ZeroPgDirectIndexedRegYAddr.calculate_unified_parameter([zero_pg], self.cpu, self.memory)
        self.assertEqual(unified_param, 20)
        self.assertEqual(self.memory.retrieve_content(unified_param), 20)

    def test_AbsDirectIndexedRegXAddr(self):
        self.cpu.state.x.set_value(10)
        low_byte = 0b1010
        high_byte = 0b1010
        self.memory.set_content(0b0000101000001010 + 10, 30)
        unified_param = AbsDirectIndexedRegXAddr.calculate_unified_parameter([low_byte, high_byte], self.cpu,
                                                                             self.memory)
        self.assertEqual(unified_param, 0b0000101000001010 + 10)
        self.assertEqual(self.memory.retrieve_content(unified_param), 30)

    def test_AbsDirectIndexedRegYAddr(self):
        self.cpu.state.y.set_value(10)
        low_byte = 0b1010
        high_byte = 0b1010
        self.memory.set_content(0b0000101000001010 + 10, 30)
        unified_param = AbsDirectIndexedRegYAddr.calculate_unified_parameter([low_byte, high_byte], self.cpu,
                                                                             self.memory)
        self.assertEqual(unified_param, 0b0000101000001010 + 10)
        self.assertEqual(self.memory.retrieve_content(unified_param), 30)

    def test_IndirectAddr(self):
        self.memory.set_content(1, 10)
        self.memory.set_content(2, 10)
        low_byte = 1
        high_byte = 0
        unified_param = IndirectAddr.calculate_unified_parameter([low_byte, high_byte], self.cpu, self.memory)
        self.assertEqual(unified_param, 0b0000101000001010)

    # addition is used - i.e. the sum is always a zero-page address.
    #    eg. FF + 2 = 0001 not 0101 as you might expect.
    #    DON'T FORGET THIS WHEN EMULATING THIS MODE
    def test_IndirectPreIndexedAddr(self):
        self.cpu.state.x.set_value(2)
        zero_pg = 0xFF
        # addition = 0b1
        self.memory.set_content(1, 3)
        self.memory.set_content(2, 3)
        unified_param = IndirectPreIndexedAddr.calculate_unified_parameter([zero_pg], self.cpu, self.memory)
        self.assertEqual(unified_param, 0b1100000011)

    def test_IndirectPostIndexedAddr(self):
        self.cpu.state.y.set_value(10)
        self.memory.set_content(1, 3)
        self.memory.set_content(2, 3)
        addr = 1
        unified_param = IndirectPostIndexedAddr.calculate_unified_parameter([addr], self.cpu, self.memory)
        self.assertEqual(unified_param, 0b1100000011 + 10)

    def test_RelativeIndexedAddr(self):
        # one byte movement offset (with signal)
        offset = 0b11111011  # -5 in 2 complement
        unified_param = RelativeIndexedAddr.calculate_unified_parameter([offset], self.cpu, self.memory)
        self.assertEqual(unified_param, offset)
