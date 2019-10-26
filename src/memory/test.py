import unittest
from src.cpu.cpu import *
from src.memory.cpu.stack import Stack
from src.memory.cpu.memory import Memory

class StackTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory(self.cpu)
        self.stack = Stack(self.memory, self.cpu.state)

    def test_push(self):
        self.stack.push_val(77)
        self.assertEqual(self.memory.retrieve_content(0x1FD), 77)
        self.assertEqual(self.cpu.state.sp.get_value(), 0xFC)

    def test_pop(self):
        self.cpu.state.sp.set_value(0xFE)
        self.memory.set_content(0x1FF, 88)
        self.assertEqual(self.stack.pop_val(), 88)
        self.assertEqual(self.cpu.state.sp.get_value(), 0xFF)

    def test_mirror_ram_first_chunk(self):
        addr = 0x312
        value = 0xFA

        self.memory.set_content(addr, value)
        self.assertEqual(self.memory.retrieve_content(addr), value)
        self.assertEqual(self.memory.retrieve_content(addr + 0x0800), value)
        self.assertEqual(self.memory.retrieve_content(addr + 0x1000), value)
        self.assertEqual(self.memory.retrieve_content(addr + 0x1800), value)

    def test_mirror_ram_second_chunk(self):
        addr = 0x0965
        value = 0xFB

        self.memory.set_content(addr, value)
        self.assertEqual(self.memory.retrieve_content(addr), value)
        self.assertEqual(self.memory.retrieve_content(addr - 0x0800), value)
        self.assertEqual(self.memory.retrieve_content(addr + 0x0800), value)
        self.assertEqual(self.memory.retrieve_content(addr + 0x1000), value)

    def test_mirror_ram_third_chunk(self):
        addr = 0x1158
        value = 0xFC

        self.memory.set_content(addr, value)
        self.assertEqual(self.memory.retrieve_content(addr), value)
        self.assertEqual(self.memory.retrieve_content(addr - 0x1000), value)
        self.assertEqual(self.memory.retrieve_content(addr - 0x0800), value)
        self.assertEqual(self.memory.retrieve_content(addr + 0x0800), value)


    def test_mirror_ram_fourth_chunk(self):
        addr = 0x1A34
        value = 0xFD

        self.memory.set_content(addr, value)
        self.assertEqual(self.memory.retrieve_content(addr), value)
        self.assertEqual(self.memory.retrieve_content(addr - 0x1800), value)
        self.assertEqual(self.memory.retrieve_content(addr - 0x1000), value)
        self.assertEqual(self.memory.retrieve_content(addr - 0x0800), value)

    def test_ppu_mirror_zero(self):
        addr = 0x2005
        value = 0xFF

        self.memory.set_content(addr, value)
        self.assertEqual(self.memory.retrieve_content(addr), value)
        self.assertEqual(self.memory.retrieve_content(addr + 8), value)
        self.assertEqual(self.memory.retrieve_content(addr + 16), value)


    def test_ppu_mirror_random(self):
        addr = 0x3A87
        value = 0xFF

        ppu_addr_intended = 0x2007

        self.memory.set_content(addr, value)
        self.assertEqual(self.memory.retrieve_content(ppu_addr_intended), value)
        self.assertEqual(self.memory.retrieve_content(ppu_addr_intended + 8), value)
        self.assertEqual(self.memory.retrieve_content(ppu_addr_intended + 16), value)
        self.assertEqual(self.memory.retrieve_content(ppu_addr_intended + 16), value)
        self.assertEqual(self.memory.retrieve_content(ppu_addr_intended + 32), value)

    def test_solve_mirroring(self):
        addr = 0x0700
        self.assertEqual(addr, self.memory.solve_mirroring(0x0700))
        self.assertEqual(addr, self.memory.solve_mirroring(0x0F00))
        self.assertEqual(addr, self.memory.solve_mirroring(0x1700))
        self.assertEqual(addr, self.memory.solve_mirroring(0x1F00))
        self.assertNotEqual(addr, self.memory.solve_mirroring(0x2700))

    def test_load_0xFFFF(self):
        addr = 0xFFFF
        a = self.memory.retrieve_content(0xFFFF)
