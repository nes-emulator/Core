# PPU command wrapper, this obj will be send to "PPU" between NMI
from .reg import *


class CommandWrapper:
    def __init__(self):
        # Temporary !
        # in the final version of this class the fields aren't intended to be ppu regs
        self.ppu_ctrl = PPUCTRL(0)
        self.ppu_mask = PPUMASK(0)
        self.ppu_status = PPUSTATUS(0)
        self.oam_addr = OAMADDR(0)
        self.oam_data = OAMDATA(0)
        self.ppu_scroll = PPUSCROLL(0)
        self.ppu_addr = PPUADDR(0)
        self.ppu_data = PPUDATA(0)
        self.oam_dma = OAMDMA(0)

    pass
    # i'm not sure about what is the best format
