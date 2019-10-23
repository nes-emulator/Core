""" having in mind the cartridge content is already stored in cartridge class,
 this class only stores the content of RAM and controller ports.
 in this version the class is not considering expansive memory through the use of banks
 """
from math import log2
from .stack import Stack
from array import array
from src.ppu.control.operation_handler import PPUOperationHandler
from src.ppu.control.reg import OAMDMA


class Memory:
    MEMORY_LIMIT = 0xFFFF + 1
    WORD_SIZE = 8
    ROM_ADDR = 0x8000
    CHROM_ADDR = 0x6000
    CHROM_SIZE = 0x2000
    PRGROM_SIZE = 0x4000
    UNSIGNED_BYTE_TYPE = 'B'
    PPU_BASE_REG_ADDR = 0x2000
    PPU_MIRROR_LIMIT = 0x3FFF

    def __init__(self, cpu, cartridge=None):
        # init a memory array
        PPUOperationHandler.init_cmd()
        self.stack = Stack(self, cpu.state)
        self.reset()
        # write all NROM data to memory
        if cartridge:
            self.loadROM(cartridge.get_prg_rom())
            if cartridge.get_chr_rom():
                self.loadCHROM(cartridge.get_chr_rom())

    def reset(self):
        # initialize memory, the content of each address is mapped to it's index
        self.memory = array(Memory.UNSIGNED_BYTE_TYPE, (0,) * Memory.MEMORY_LIMIT)

    @PPUOperationHandler.ppu_read_verifier
    def retrieve_content(self, addr):
        if not Memory._valid_memory_word(addr, Memory.WORD_SIZE * 2):
            pass
        # print("Invalid memory access, indexing address > 16bits, word = 16bits")
        return self.memory[addr]

    @PPUOperationHandler.ppu_write_verifier
    def set_content(self, addr, val):
        if not Memory._valid_memory_word(val, Memory.WORD_SIZE):
            pass
            # raise("Invalid memory storage, value stored > 16bits, word = 16bits")
        if not Memory._valid_memory_word(addr, Memory.WORD_SIZE * 2):
            pass
            # raise("Invalid memory storage, indexing address > 16bits, word = 16bits")
        if addr > Memory.ROM_ADDR:
            pass
            # raise("invalid memory storage, you cant store data in ROM")
        self.memory[addr] = val
        self.apply_memory_mirror(addr, val)

    def loadCHROM(self, rom_data):
        arr_chr = array(Memory.UNSIGNED_BYTE_TYPE, rom_data)
        self.memory[self.CHROM_ADDR:(self.CHROM_ADDR + self.CHROM_SIZE)] = arr_chr

    def loadROM(self, rom_data):
        arr_rom = array(Memory.UNSIGNED_BYTE_TYPE, rom_data)
        self.memory[self.ROM_ADDR:(self.ROM_ADDR + self.PRGROM_SIZE)] = arr_rom
        self.memory[(self.ROM_ADDR + self.PRGROM_SIZE):(self.ROM_ADDR + 2 * self.PRGROM_SIZE)] = arr_rom

    @classmethod
    def _valid_memory_word(cls, val, size):
        return log2(abs(val)) < size if val != 0 else True

    # Checks if a address is RAM Mirrored and returns the actual address
    def solve_mirroring(self, addr):
        if addr <= 0x0800:
            return addr
        elif addr <= 0x0FFF:
            return addr - 0x0800
        elif addr <= 0x17FF:
            return addr - 0x1000
        elif addr <= 0x1FFF:
            return addr - 0x1800
        else:  # These are PPU addresses
            return addr

    def apply_memory_mirror(self, addr, val):
        if addr <= 0x0800:
            self.apply_ram_mirror(addr, val)
        elif addr <= 0x0FFF:
            self.apply_ram_mirror(addr - 0x0800, val)
        elif addr <= 0x17FF:
            self.apply_ram_mirror(addr - 0x1000, val)
        elif addr <= 0x1FFF:
            self.apply_ram_mirror(addr - 0x1800, val)

        if addr >= 0x2000 and addr <= 0x3FFF:
            self.apply_ppu_register_mirror(addr, val)

    def apply_ram_mirror(self, addr, val):
        self.memory[addr] = val
        self.memory[addr + 0x0800] = val
        self.memory[addr + 0x1000] = val
        self.memory[addr + 0x1800] = val

    def apply_ppu_register_mirror(self, addr, val):
        ppu_reg_size = 8
        ppu_reg = (addr % ppu_reg_size) + 0x2000

        while ppu_reg <= 0x3FFF:
            self.memory[ppu_reg] = val
            ppu_reg += ppu_reg_size

    @classmethod
    # if addr is associated with a ppu reg, the reg number is returned
    def ppu_reg(cls, addr):
        if addr == OAMDMA.BASE_ADDR:
            return 9
        if addr > cls.PPU_MIRROR_LIMIT:
            return -1
        reg = (addr - (Memory.PPU_BASE_REG_ADDR)) % 8
        if 0 <= reg <= 7:
            return reg
        return -1

    @classmethod
    def reverse_ppu_mirroring(cls, addr):
        pass
