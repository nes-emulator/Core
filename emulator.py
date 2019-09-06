import sys

from src.mapper import *
from src.cartridge import *


class Emulator():
    def __init__(self, cartridge_path):
        try:
            self.cart = Cartridge(cartridge_path)

            if self.cart.get_mapper_type() == MapperType.NROM:
                self.mapper = NromMapper(self.cart)
            else:
                raise ValueError("Cartridge specifies a mapper type not supported yet")
        except ValueError as err:
            print("ERROR: ", end="")
            print(err.args)


def main(path):
    # emulator = Emulator(path)
    print("BATATA")


# ENTRY POINT
if __name__ == "__main__":
    if (len(sys.argv) < 2):
        sys.exit(1)
    main(sys.argv[1])
