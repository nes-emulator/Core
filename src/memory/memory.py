""" having in mind the cartridge content is already stored in cartridge class,
 this class only stores the content of RAM and controller ports.
 in this version the class is not considering expansive memory through the use of banks
 """
from math import log2


class Memory:
    MEMORY_LIMIT = 0xFFFF
    WORD_SIZE = 8
    ROM_ADDR = 0x8000

    def __init__(self, cartridge=None):
        # init a memory array
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
            raise ("Invalid memory access, indexing address > 16bits, word = 16bits")
        return self.memory[addr]

    def set_content(self, addr, val):
        if not Memory._valid_memory_word(val, Memory.WORD_SIZE):
            raise ("Invalid memory storage, value stored > 16bits, word = 16bits")
        if not Memory._valid_memory_word(addr, Memory.WORD_SIZE * 2):
            raise ("Invalid memory storage, indexing address > 16bits, word = 16bits")
        if addr > Memory.ROM_ADDR:
            raise ("invalid memory storage, you cant store data in ROM")
        self.memory[addr] = val

    def loadROM(self, rom_data):
        self.memory[self.ROM_ADDR:] = list(rom_data)

    @classmethod
    def _valid_memory_word(cls, val, size):
        return log2(val) + 1 < size if val > 0 else True
