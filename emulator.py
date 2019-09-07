import sys

from src.mapper import *
from src.cartridge import *


class Emulator():
    def __init__(self, cartridge_path="game/game.bin"):

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


def main(path):
    if (path):
        emulator = Emulator(path)
    else:
        emulator = Emulator()
    cartridge = emulator.cart
    rom = cartridge.prg_rom
    for instr in rom:
        print(format(int(instr), "08b"))


# ENTRY POINT
if __name__ == "__main__":
    if (len(sys.argv) < 2):
        main(None)
    else:
        main(sys.argv[1])
