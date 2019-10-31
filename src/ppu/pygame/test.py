import unittest
from src.ppu.pygame.controller import Controllers
from src.memory.cpu.memory import Memory
from src.cpu.cpu import CPU
from multiprocessing import Process


def register_ctrl_event(ctrl1_state, ctrl2_state):
    ctrl1_state[0] = 1
    ctrl1_state[1] = 0
    ctrl1_state[2] = 1
    ctrl1_state[3] = 0
    ctrl1_state[4] = 1
    ctrl1_state[5] = 0
    ctrl1_state[6] = 1
    ctrl1_state[7] = 0

    ctrl2_state[0] = 1
    ctrl2_state[1] = 1
    ctrl2_state[2] = 1
    ctrl2_state[3] = 1
    ctrl2_state[4] = 1
    ctrl2_state[5] = 1
    ctrl2_state[6] = 1
    ctrl2_state[7] = 1


class ControlerCPUTests(unittest.TestCase):
    def setUp(self):
        cpu = CPU()
        self.memory = Memory(cpu)

    def test_ctl_load(self):
        p = Process(target=register_ctrl_event, args=(Controllers.ctrl1_btn_states, Controllers.ctrl2_btn_states,))
        p.start()
        p.join()
        self.memory.set_content(Controllers.CTRL1_ADDR, 1)
        self.memory.set_content(Controllers.CTRL2_ADDR, 1)
        for _ in range(4):
            self.assertEqual(0b1, self.memory.retrieve_content(Controllers.CTRL1_ADDR))
            self.assertEqual(0b0, self.memory.retrieve_content(Controllers.CTRL1_ADDR))
        for _ in range(8):
            self.assertEqual(0b1, self.memory.retrieve_content(Controllers.CTRL2_ADDR))

    def test_ctl_read(self):
        p = Process(target=register_ctrl_event, args=(Controllers.ctrl1_btn_states, Controllers.ctrl2_btn_states,))
        p.start()
        p.join()
        self.memory.set_content(Controllers.CTRL1_ADDR, 1)
        self.memory.set_content(Controllers.CTRL2_ADDR, 1)
        for _ in range(4):
            self.assertEqual(0b1, self.memory.retrieve_content(Controllers.CTRL1_ADDR))
            self.assertEqual(0b0, self.memory.retrieve_content(Controllers.CTRL1_ADDR))
        self.assertEqual(0b1, self.memory.retrieve_content(Controllers.CTRL1_ADDR))
        for _ in range(8):
            self.assertEqual(0b1, self.memory.retrieve_content(Controllers.CTRL2_ADDR))
        for _ in range(8):
            self.assertEqual(0b0, self.memory.retrieve_content(Controllers.CTRL2_ADDR))
            self.assertEqual(0b0, self.memory.retrieve_content(Controllers.CTRL1_ADDR))