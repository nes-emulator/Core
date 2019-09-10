""" having in mind the cartridge content is already stored in cartridge class,
 this class only stores the content of RAM and controller ports.
 in this version the class is not considering expansive memory through the use of banks
 """


class RamMemory:
    MEMORY_LIMIT = 0x8000

    def __init__(self):
        # is it necessary to distinguish between all regions (ROM,RAM,flags , etc) or one global memory is good enough ?
        self.memory = []
        self.reset()

    def reset(self):
        self.memory = [0b00000000] * self.MEMORY_LIMIT  # initialize memory, the content of each address is mapped to it's index

    def retrieve_content(self, addr):
        return self.memory[addr];

    def set_content(self, addr, val):
        self.memory[addr] = val


