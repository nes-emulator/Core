import unittest
from .addressing import *
from src.cpu.cpu import CPU
from src.memory.memory import Memory



class InstructionAddressingTest(unittest.TestCase):

    def setUp(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.memory.reset()


    def test_ImmediateAddr(self):
        parameter = [50]

        pass

    def test_ZeroPageAddr(self):
        pass

    def test_AbsoluteAddr(self):
        pass

    def test_ImpliedAddr(self):
        pass

    def test_AccumulatorAddr(self):
        pass

    def test_AbsDirectIndexedAddr(self):
        pass

    def test_ZeroPgDirectIndexedRegXAddr(self):
        pass

    def tets_ZeroPgDirectIndexedRegYAddr(self):
        pass

    def test_AbsDirectIndexedRegXAddr(self):
        pass

    def test_AbsDirectIndexedRegYAddr(self):
        pass

    def test_IndirectAddr(self):
        pass

    def test_IndirectPreIndexedAddr(self):
        pass

    def test_IndirectPostIndexedAddr(self):
        pass

    def test_RelativeIndexedAddr(self):
        pass
