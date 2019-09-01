from mapper import *
from cartridge import *

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


emulator = Emulator('/home/joe/Documents/emulator/game/game.nes')
