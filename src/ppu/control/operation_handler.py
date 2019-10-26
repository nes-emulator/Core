from .callback import PPURegCallback
# import all Regs
from .reg import PPUCTRL, PPUMASK, PPUSTATUS, OAMADDR, OAMDATA, PPUSCROLL, PPUADDR, PPUDATA, OAMDMA


class PPUOperationHandler:
    # ppu reg addr: callback
    write_operations = {PPUCTRL.BASE_ADDR: PPURegCallback.ctrl_write,
                        PPUMASK.BASE_ADDR: PPURegCallback.mask_write,
                        OAMADDR.BASE_ADDR: PPURegCallback.oam_addr_write,
                        OAMDATA.BASE_ADDR: PPURegCallback.oam_addr_write,
                        PPUSCROLL.BASE_ADDR: PPURegCallback.scroll_write,
                        PPUADDR.BASE_ADDR: PPURegCallback.ppu_addr_write,
                        PPUDATA.BASE_ADDR: PPURegCallback.ppu_data_write,
                        OAMDMA.BASE_ADDR: PPURegCallback.oam_dma_write
                        }

    read_operations = {PPUSTATUS.BASE_ADDR: PPURegCallback.status_read,
                       OAMDATA.BASE_ADDR: PPURegCallback.oam_data_read,
                       PPUADDR.BASE_ADDR: PPURegCallback.ppu_addr_read,
                       PPUDATA.BASE_ADDR: PPURegCallback.ppu_data_read,
                       }

    @classmethod
    def extract_reg_data(cls, reg_addr, mem):
        pass

    # if addr is a PPU reg, return addr or None
    @classmethod
    def accessed_reg(cls, operations, addr, memory):
        ppu_reg = memory.ppu_reg(addr)
        if ppu_reg == -1:
            return  # None, invalid
        reg_addr = ppu_reg + memory.PPU_BASE_REG_ADDR if ppu_reg != 9 else OAMDMA.BASE_ADDR
        if not reg_addr in operations:
            return  # None, invalid
        return reg_addr

    # PPU memory manipulation decorators, map the action to a proper method to handle
    @classmethod
    def ppu_write_verifier(cls, memory_access_func):
        def manipulation_wrapper(memory, addr, val):
            memory_access_func(memory, addr, val)
            reg_addr = cls.accessed_reg(cls.write_operations, addr, memory)
            # maps the action
            if reg_addr:
                handler = cls.write_operations[reg_addr]
                handler(memory)

        return manipulation_wrapper

    @classmethod
    def ppu_read_verifier(cls, memory_access_func):
        def manipulation_wrapper(memory, addr):
            mem_val = memory_access_func(memory, addr)
            reg_addr = cls.accessed_reg(cls.read_operations, addr, memory)
            # maps the action
            if reg_addr:
                handler = cls.read_operations[reg_addr]
                handler(memory)
            return mem_val

        return manipulation_wrapper
