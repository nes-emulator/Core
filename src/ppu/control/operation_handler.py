from .command_wrapper import CommandWrapper
from .callback import PPURegCallback
# import all Regs
from .reg import PPUCTRL, PPUMASK, PPUSTATUS, OAMADDR, OAMDATA, PPUSCROLL, PPUADDR, PPUDATA, OAMDMA


class PPUOperationHandler:
    current_cmd = None
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
    def init_cmd(cls):
        cls.current_cmd = CommandWrapper()

    @classmethod
    def extract_reg_data(cls, reg_addr, mem):
        pass

    # PPU memory manipulation decorators, map the action to a proper method to handle
    @classmethod
    def ppu_write_verifier(cls, memory_access_func):
        def manipulation_wrapper(memory, addr, val):
            memory_access_func(memory, addr, val)
            ppu_reg = memory.ppu_reg(addr)
            # maps the action
            if ppu_reg > 0:
                reg_addr = ppu_reg + memory.PPU_BASE_REG_ADDR
                if reg_addr in cls.write_operations:
                    handler = cls.write_operations[reg_addr]
                    cls.current_cmd = handler(memory, cls.current_cmd)

        return manipulation_wrapper

    @classmethod
    def ppu_read_verifier(cls, memory_access_func):
        def manipulation_wrapper(memory, addr):
            mem_val = memory_access_func(memory, addr)
            ppu_reg = memory.ppu_reg(addr)
            # maps the action
            if ppu_reg > 0:
                reg_addr = ppu_reg + memory.PPU_BASE_REG_ADDR
                if reg_addr in cls.read_operations:
                    handler = cls.read_operations[reg_addr]
                    cls.current_cmd = handler(memory, cls.current_cmd)
            return mem_val

        return manipulation_wrapper
