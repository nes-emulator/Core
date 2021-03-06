""" having in mind the cartridge content is already stored in cartridge class,
 this class only stores the content of RAM and controller ports.
 in this version the class is not considering expansive memory through the use of banks
 """
from math import log2
from .stack import Stack
from array import array
from src.ppu.control.operation_handler import PPUOperationHandler
from src.ppu.control.reg import OAMDMA
from src.memory.ppu.PPUMemory import PPUMemory
from src.memory.apu.APUMemory import APUMemory
from src.ppu.pygame.controller import Controllers


class Memory:
    MEMORY_LIMIT = 0xFFFF + 1
    WORD_SIZE = 8
    ROM_ADDR = 0x8000
    CHROM_ADDR = 0x6000
    CHROM_SIZE = 0x2000
    PRGROM_SIZE = 0x4000
    UNSIGNED_BYTE_TYPE = 'B'
    PPU_BASE_REG_ADDR = 0x2000
    PPU_MIRROR_LIMIT = 0x2007

    def __init__(self, cpu, cartridge=None):
        self.ppu_memory = PPUMemory()
        self.apu_memory = APUMemory()
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

    @Controllers.read_button
    @PPUOperationHandler.ppu_read_verifier
    def retrieve_content(self, addr):
        return self.memory[addr]

    @Controllers.btn_loader
    @PPUOperationHandler.ppu_write_verifier
    def set_content(self, addr, val):
        val %= 256
        self.memory[addr] = val
        self.apply_memory_mirror(addr, val)
        self.apu_memory.set_reg(addr, val)

    def loadCHROM(self, rom_data):
        arr_chr = array(Memory.UNSIGNED_BYTE_TYPE, rom_data)
        #self.memory[self.CHROM_ADDR:(self.CHROM_ADDR + self.CHROM_SIZE)] = arr_chr

    def loadROM(self, rom_data):
        arr_rom = array(Memory.UNSIGNED_BYTE_TYPE, rom_data)
        if len(arr_rom) == self.PRGROM_SIZE:
            self.memory[self.ROM_ADDR:(self.ROM_ADDR + self.PRGROM_SIZE)] = arr_rom
            self.memory[(self.ROM_ADDR + self.PRGROM_SIZE):(self.ROM_ADDR + 2 * self.PRGROM_SIZE)] = arr_rom
        else:
            self.memory[self.ROM_ADDR:self.ROM_ADDR + len(arr_rom)] = arr_rom

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
        ppu_reg = (addr - 0x2000) % 8
        ppu_reg += 0x2000

        while ppu_reg <= 0x3FFF:
            self.memory[ppu_reg] = val
            ppu_reg += 8

    @classmethod
    # if addr is associated with a ppu reg, the reg number is returned
    def ppu_reg(cls, addr):
        if addr == OAMDMA.BASE_ADDR:
            return 9

        if addr < 0x2000 or addr > 0x3FFF:
            return -1

        reg = (addr - Memory.PPU_BASE_REG_ADDR) % 8
        return reg
