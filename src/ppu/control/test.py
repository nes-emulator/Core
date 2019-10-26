import unittest
from multiprocessing import Process, Array


def f(a, b, c):
    while a[0] == 0 or b[0] == 0 or c[0] == 0:
        pass


class SharedMemoryTest(unittest.TestCase):

    def setUp(self):
        self.mem1 = Array('B', (0,) * 2)
        self.mem2 = Array('B', (0,) * 2)
        self.mem3 = Array('B', (0,) * 2)

    def test_manipulation(self):
        p = Process(target=f, args=(self.mem1, self.mem2, self.mem3,))
        p.start()
        self.mem1[0] = 1
        self.mem2[0] = 1
        self.mem3[0] = 1
        p.join()
