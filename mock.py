import sys

from src.mapper import *
from src.memory.cartridge import *
from src.memory.cpu.memory import Memory
from src.cpu.cpu import CPU
from src.cpu.instruction_runner import Runner
from src.instruction.collection import InstructionCollection
from src.util.util import *
from src.ppu.pygame.screen_controller import ScreenController

def read_sprite_row(channel_a, channel_b):
    bits_a = extract_8_bits(channel_a)
    bits_b = extract_8_bits(channel_b)
    return [sum(e) for e in zip(bits_a, map(lambda x: x*2, bits_b))]

def get_sprites(chr_rom):
    idx = 0
    sprites = []
    for _ in range(512):
        sprite = []
        channel_a = chr_rom[idx : idx + 8]
        channel_b = chr_rom[idx + 8 : idx + 16]
        for i in range(8):
            sprite.append(read_sprite_row(channel_a[i], channel_b[i]))

        idx += 16
        sprites.append(sprite)

    return sprites


class Emulator():
    def __init__(self, cartridge_path):
        self.cpu = CPU()
        self.memory = None
        self.cart = None
        self.mapper = None
        # self.instructions = None
        self.chr_rom = None

        try:

            self.cart = Cartridge(cartridge_path)
            self.chr_rom = self.cart.get_chr_rom()

            sprites = get_sprites(self.chr_rom)

            game = ScreenController([0] * 0x4000)
            game.set_sprites(sprites)
            while True:
                game.init_info()
                game.draw_background()
                pass

            # self.instructions = self.cart.get_prg_rom()
            #
            # if self.cart.get_mapper_type() == MapperType.NROM:
            #     self.mapper = NromMapper(self.cart)
            # else:
            #     raise ValueError("Cartridge specifies a mapper type not supported yet")
            #
            # InstructionCollection.initialize()
            # Runner.run(self.instructions, self.cpu, self.memory)

        except Exception as err:
            print(e)
            print(err.args)


def main(path="game/game.bin"):
    emulator = Emulator(path)


# ENTRY POINT
if __name__ == "__main__":
    try:
        if (len(sys.argv) < 2):
            main()
        elif len(sys.argv) == 2:
            main(sys.argv[1])
        else:
            Runner.log_as_nestest()
            main(sys.argv[1])
    except Exception as e:
        sys.exit(0)
