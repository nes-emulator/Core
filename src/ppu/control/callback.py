from src.ppu.control.command_wrapper import CommandWrapper
from src.util.util import make_16b_binary
from .reg import *


class PPURegCallback:

    @staticmethod
    def ctrl_write(memory, cmd_wrapper) -> CommandWrapper:
        return cmd_wrapper

    @staticmethod
    def mask_write(memory, cmd_wrapper) -> CommandWrapper:
        return cmd_wrapper

    @staticmethod
    def status_read(memory, cmd_wrapper) -> CommandWrapper:
        cmd_wrapper.ppu_status.v = False
        memory.set_content(PPUSTATUS.BASE_ADDR, cmd_wrapper.ppu_status.to_val())
        return cmd_wrapper

    @staticmethod
    def oam_addr_write(memory, cmd_wrapper) -> CommandWrapper:
        return cmd_wrapper

    @staticmethod
    def oam_data_read(memory, cmd_wrapper) -> CommandWrapper:
        return cmd_wrapper

    @staticmethod
    def oam_data_write(memory, cmd_wrapper) -> CommandWrapper:
        return cmd_wrapper

    @staticmethod  # write twice
    def scroll_write(memory, cmd_wrapper) -> CommandWrapper:
        return cmd_wrapper

    @staticmethod  # write twice
    def ppu_addr_write(memory, cmd_wrapper) -> CommandWrapper:
        return cmd_wrapper

    @staticmethod
    def ppu_addr_read(memory, cmd_wrapper) -> CommandWrapper:
        return cmd_wrapper

    @staticmethod
    def ppu_data_read(memory, cmd_wrapper) -> CommandWrapper:
        return cmd_wrapper

    @staticmethod
    def ppu_data_write(memory, cmd_wrapper) -> CommandWrapper:
        return cmd_wrapper

    # XX00-$XXFF to 0200-$02FF
    @staticmethod
    def oam_dma_write(memory, cmd_wrapper) -> CommandWrapper:
        val = memory.memory[OAMDMA.BASE_ADDR]
        low_from = make_16b_binary(val, 0x00)
        high_from = make_16b_binary(val, 0xFF) + 1
        for from_addr, to_addr in zip(range(low_from, high_from), range(0x200, 0x02FF + 1)):
            memory.memory[to_addr] = memory.memory[from_addr]
        return cmd_wrapper
