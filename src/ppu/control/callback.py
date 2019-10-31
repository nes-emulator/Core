from src.util.util import make_16b_binary
from .reg import *


class PPURegCallback:
    scroll_second_write = False
    ppu_addr_second_write = False
    addr_high_byte = 0
    pointer_address = 0x0

    @staticmethod
    def ctrl_write(memory):
        # write to mapped reg
        memory.ppu_memory.get_regs()[PPUCTRL.BASE_ADDR - BASE_ADDR] = memory.memory[PPUCTRL.BASE_ADDR]

    @staticmethod
    def mask_write(memory):
        # write to mapped reg
        memory.ppu_memory.get_regs()[PPUMASK.BASE_ADDR - BASE_ADDR] = memory.memory[PPUMASK.BASE_ADDR]
        pass

    @classmethod
    def status_read(cls, memory):
        # change NMI bit
        status = PPUSTATUS(memory.memory[PPUSTATUS.BASE_ADDR])
        status.v = True
        # reset PPUSCROLL and PPUDATA
        memory.set_content(PPUSCROLL.BASE_ADDR, 0)
        memory.ppu_memory.get_regs()[PPUSCROLL.BASE_ADDR - BASE_ADDR] = 0
        memory.ppu_memory.get_regs()[PPUADDR.BASE_ADDR - BASE_ADDR] = 0
        memory.memory[PPUADDR.BASE_ADDR] = 0
        cls.ppu_addr_second_write = False
        # save new status reg
        memory.set_content(PPUSTATUS.BASE_ADDR, status.to_val())
        memory.ppu_memory.get_regs()[PPUSTATUS.BASE_ADDR - BASE_ADDR] = status.to_val()
        pass

    #transfer OAM[OAMADDR] to OAMDATA
    @staticmethod
    def oam_addr_write(memory):
        # ???
        memory.ppu_memory.get_regs()[OAMADDR.BASE_ADDR - BASE_ADDR] = memory.memory[OAMADDR.BASE_ADDR]
        pass

    @staticmethod
    def oam_data_read(memory):
        # OK
        pass

    @staticmethod
    def oam_data_write(memory):
        oam_addr = memory.memory[OAMADDR.BASE_ADDR]
        oam_addr += 1
        #memory.set_content(OAMADDR.BASE_ADDR, oam_addr)
        #memory.ppu_memory.get_regs()[OAMDATA.BASE_ADDR - BASE_ADDR] = memory.memory[OAMDATA.BASE_ADDR]
        memory.ppu_memory.get_regs()[OAMADDR.BASE_ADDR - BASE_ADDR] = oam_addr
        pass

    # bottleneck, ppu should notify that it received the first write
    # the addres can be maped to PPUSCROLL(reg 5) Y and PPUSCROLL X(reg 9)
    @classmethod  # write twice
    def scroll_write(cls, memory):
        if cls.scroll_second_write:  # second write
            cls.scroll_second_write = False
            memory.ppu_memory.get_regs()[8] = memory.ppu_memory.get_regs()[PPUSCROLL.BASE_ADDR - BASE_ADDR]  # reg 9 = reg 5  X
            memory.ppu_memory.get_regs()[PPUSCROLL.BASE_ADDR - BASE_ADDR] = memory.memory[PPUSCROLL.BASE_ADDR]  # reg 5 = Y
        else:  # first write
            cls.scroll_second_write = True
            memory.ppu_memory.get_regs()[PPUSCROLL.BASE_ADDR - BASE_ADDR] = memory.memory[PPUSCROLL.BASE_ADDR]  # reg 5 X
        # final state - > reg5 = Y ; reg9= X

    # transfer data to ppu memory
    @classmethod  # write twice
    def ppu_addr_write(cls, memory):

        # write to mapped reg
        memory.ppu_memory.get_regs()[PPUADDR.BASE_ADDR - BASE_ADDR] = memory.memory[PPUADDR.BASE_ADDR]

        # check the 'write twice' and updates VRAM pointer
        if cls.ppu_addr_second_write:
            cls.ppu_addr_second_write = False
            addr = make_16b_binary(cls.addr_high_byte, memory.memory[PPUADDR.BASE_ADDR])
            cls.pointer_address = addr
        else:
            cls.ppu_addr_second_write = True
            cls.addr_high_byte = memory.memory[PPUADDR.BASE_ADDR]

    @staticmethod
    def ppu_addr_read(memory):
        pass

    @staticmethod
    def ppu_data_read(memory):
        ppuctrl = PPUCTRL(memory.memory[PPUCTRL.BASE_ADDR])
        # status.increment_mode = not status.increment_mode
        # reads updates VRAM pointer
        cls.pointer_address += ppuctrl.extract_vram_increment

    @classmethod
    def ppu_data_write(cls, memory):
        memory.ppu_memory.get_regs()[PPUDATA.BASE_ADDR - BASE_ADDR] = memory.memory[PPUDATA.BASE_ADDR]
        status = PPUCTRL(memory.memory[PPUCTRL.BASE_ADDR])
        status.increment_mode = not status.increment_mode
        memory.ppu_memory.set_val_memory(cls.pointer_address, memory.memory[PPUDATA.BASE_ADDR])
        cls.pointer_address += 1

    # XX00-$XXFF to OAM
    @staticmethod
    def oam_dma_write(memory):
        val = memory.memory[OAMDMA.BASE_ADDR]
        low_from = make_16b_binary(val, 0x00)
        high_from = make_16b_binary(val, 0xFF) + 1
        for from_addr, to_addr in zip(range(low_from, high_from), range(0, 256)):
            memory.ppu_memory.set_val_oam(to_addr,memory.memory[from_addr])
