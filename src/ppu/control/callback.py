from src.util.util import make_16b_binary
from .reg import *


class PPURegCallback:

    @staticmethod
    def ctrl_write(memory):
        # write to mapped reg
        memory.ppu_memory.get_regs()[PPUCTRL.BASE_ADDR - BASE_ADDR] = memory.memory[PPUCTRL.BASE_ADDR]
        pass

    @staticmethod
    def mask_write(memory):
        # write to mapped reg
        memory.ppu_memory.get_regs()[PPUMASK.BASE_ADDR - BASE_ADDR] = memory.memory[PPUMASK.BASE_ADDR]
        pass

    @staticmethod
    def status_read(memory):
        # cmd_wrapper.ppu_status.v = False
        # memory.set_content(PPUSTATUS.BASE_ADDR.ppu_status.to_val())
        pass

    @staticmethod
    def oam_addr_write(memory):
        # write to mapped reg
        memory.ppu_memory.get_regs()[OAMADDR.BASE_ADDR - BASE_ADDR] = memory.memory[OAMADDR.BASE_ADDR]
        pass

    @staticmethod
    def oam_data_read(memory):
        pass

    @staticmethod
    def oam_data_write(memory):
        # write to mapped reg
        memory.ppu_memory.get_regs()[OAMDATA.BASE_ADDR - BASE_ADDR] = memory.memory[OAMDATA.BASE_ADDR]
        pass

    @staticmethod  # write twice
    def scroll_write(memory):
        # ????
        pass

    @staticmethod  # write twice
    def ppu_addr_write(memory):
        # write to mapped reg
        # ????
        pass

    @staticmethod
    def ppu_addr_read(memory):
        pass

    @staticmethod
    def ppu_data_read(memory):
        pass

    @staticmethod
    def ppu_data_write(memory):
        memory.ppu_memory.get_regs()[BASE_ADDR - PPUDATA.BASE_ADDR] = memory.memory[PPUDATA.BASE_ADDR]
        # write to mapped reg
        pass

    # XX00-$XXFF to 0200-$02FF
    @staticmethod
    def oam_dma_write(memory):
        val = memory.memory[OAMDMA.BASE_ADDR]
        low_from = make_16b_binary(val, 0x00)
        high_from = make_16b_binary(val, 0xFF) + 1
        for from_addr, to_addr in zip(range(low_from, high_from), range(0x200, 0x02FF + 1)):
            memory.memory[to_addr] = memory.memory[from_addr]
        pass
