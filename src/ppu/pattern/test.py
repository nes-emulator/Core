import unittest
from src.cpu.cpu import CPU
from src.memory.memory import Memory
from .pattern_table import PatternTable

class PatternTableTest(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory(self.cpu)

    def test_pattern_table_simple(self):
        self.memory.set_content(0x0000, 0x41)
        self.memory.set_content(0x0001, 0xC2)
        self.memory.set_content(0x0002, 0x44)
        self.memory.set_content(0x0003, 0x48)
        self.memory.set_content(0x0004, 0x10)
        self.memory.set_content(0x0005, 0x20)
        self.memory.set_content(0x0006, 0x40)
        self.memory.set_content(0x0007, 0x80)
        self.memory.set_content(0x0008, 0x01)
        self.memory.set_content(0x0009, 0x02)
        self.memory.set_content(0x000A, 0x04)
        self.memory.set_content(0x000B, 0x08)
        self.memory.set_content(0x000C, 0x16)
        self.memory.set_content(0x000D, 0x21)
        self.memory.set_content(0x000E, 0x42)
        self.memory.set_content(0x000F, 0x87)

        table = PatternTable()
        table.get_all_tiles(self.memory)

        pattern = table.pattern
        self.assertEqual(256 * 64, len(pattern))

        self.assertEqual(1, pattern[1])
        self.assertEqual(3, pattern[7])
        self.assertEqual(1, pattern[1 * 8 + 0])
        self.assertEqual(1, pattern[1 * 8 + 1])
        self.assertEqual(3, pattern[1 * 8 + 6])
        self.assertEqual(1, pattern[2 * 8 + 1])
        self.assertEqual(3, pattern[2 * 8 + 5])
        self.assertEqual(1, pattern[3 * 8 + 1])
        self.assertEqual(3, pattern[3 * 8 + 4])
        self.assertEqual(3, pattern[4 * 8 + 3])
        self.assertEqual(2, pattern[4 * 8 + 5])
        self.assertEqual(2, pattern[4 * 8 + 6])
        self.assertEqual(3, pattern[5 * 8 + 2])
        self.assertEqual(2, pattern[5 * 8 + 7])
        self.assertEqual(3, pattern[6 * 8 + 1])
        self.assertEqual(2, pattern[6 * 8 + 6])
        self.assertEqual(3, pattern[7 * 8 + 0])
        self.assertEqual(2, pattern[7 * 8 + 5])
        self.assertEqual(2, pattern[7 * 8 + 6])
        self.assertEqual(2, pattern[7 * 8 + 7])

        # Intended first tile from pattern table
        # 01234567
        # .1.....3
        # 11....3.
        # .1...3..
        # .1..3...
        # ...3.22.
        # ..3....2
        # .3....2.
        # 3....222