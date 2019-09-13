import sys

from src.mapper import *
from src.memory.cartridge import *
from src.memory.memory import RamMemory
from src.cpu.cpu import CPU


class Emulator():
    def __init__(self, cartridge_path):
        self.cpu = CPU();
        self.memory = RamMemory();
        self.cart = None
        self.mapper = None
        self.instructions = None

        try:
            self.cart = Cartridge(cartridge_path)
            self.instructions = self.cart.get_prg_rom()

            if self.cart.get_mapper_type() == MapperType.NROM:
                self.mapper = NromMapper(self.cart)
            else:
                raise ValueError("Cartridge specifies a mapper type not supported yet")
        except ValueError as err:
            print("ERROR: ", end="")
            print(err.args)


def main(path="game/game.bin"):
    emulator = Emulator(path)
    emulator.cart.print_prg_as_binary()


# ENTRY POINT
if __name__ == "__main__":
    if (len(sys.argv) < 2):
        main()
    else:
        main(sys.argv[1])
