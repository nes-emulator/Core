""" having in mind the cartridge content is already stored in cartridge class,
 this class only stores the content of RAM and controller ports.
 in this version the class is not considering expansive memory through the use of banks
 """
from math import log2
from .stack import Stack


class Memory:
    MEMORY_LIMIT = 0xFFFF
    WORD_SIZE = 8
    ROM_ADDR = 0x8000

    def __init__(self, cpu, cartridge=None):
        # init a memory array
        self.stack = Stack(self, cpu.state)
        self.memory = []
        self.reset()
        # write all NROM data to memory
        if cartridge:
            rom = cartridge.get_prg_rom() + cartridge.get_chr_rom()
            self.loadROM(rom)

    def reset(self):
        # initialize memory, the content of each address is mapped to it's index
        self.memory = [0] * Memory.MEMORY_LIMIT

    def retrieve_content(self, addr):
        if not Memory._valid_memory_word(addr, Memory.WORD_SIZE * 2):
            pass
        # print("Invalid memory access, indexing address > 16bits, word = 16bits")

        return self.memory[addr]

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

    def loadROM(self, rom_data):
        lst_rom = list(rom_data)
        rom_size = len(lst_rom)
        self.memory[self.ROM_ADDR:self.ROM_ADDR + rom_size] = lst_rom
        self.memory[(self.ROM_ADDR + rom_size):(self.ROM_ADDR + 2 * rom_size)] = lst_rom

    @classmethod
    def _valid_memory_word(cls, val, size):
        return log2(abs(val)) < size if val != 0 else True
