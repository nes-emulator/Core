from src.ppu.control.ppu_init import PPU_Runner_Initializer

class APUMemory:
    NUM_REGS = 18
    BASE_ADDR = 0x4000

    def __init__(self):
        self.regs = PPU_Runner_Initializer.mp_context.Array('B', (0,) * APUMemory.NUM_REGS, lock=False)

    def get_regs(self):
        return self.regs

    def set_reg(self, addr, value):

        index = addr - APUMemory.BASE_ADDR

        if index < 0 or index >= APUMemory.NUM_REGS:
            return

        if index == 8:
            print(value)

        self.regs[index] = value
