import unittest
from src.cpu.cpu import *
from src.memory.stack import Stack
from src.memory.memory import Memory

class StackTest(unittest.TestCase):
    def setUp(self):
        self.memory = Memory()
        self.cpu = CPU()
        self.stack = Stack(self.memory, self.cpu.state)

    def test_push(self):
        self.stack.push_val(77)
        self.assertEqual(self.memory.retrieve_content(0x1FF), 77)
        self.assertEqual(self.cpu.state.sp.get_value(), 0x1FE)

    def test_pop(self):
        self.cpu.state.sp.set_value(0x1FE)
        self.memory.set_content(0x1FF, 88)
        self.assertEqual(self.stack.pop_val(), 88)
        self.assertEqual(self.cpu.state.sp.get_value(), 0x1FF)
