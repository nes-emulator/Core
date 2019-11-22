from src.ppu.control.ppu_init import PPU_Runner_Initializer
from src.register.register import Register

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

        # # APU Callbacks
        # if index == 15:
        #     reg = Register(value)
        #     # Writing a zero to any of the channel enable bits will silence that
        #     # channel and set its length counter to 0
        #     if not reg.get_bit(0):
        #         sq1 = Register(self.regs[3])
        #         sq1.change_bits(3, [0, 0, 0, 0, 0])
        #     if not reg.get_bit(1):
        #         sq2 = Register(self.regs[7])
        #         sq2.change_bits(3, [0, 0, 0, 0, 0])
        #     # TODO: tri and noise

        # write to PPU memory
        self.regs[index] = value
