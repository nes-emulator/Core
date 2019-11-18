import sys

from src.mapper import *
from src.memory.cartridge import *
from src.memory.cpu.memory import Memory
from src.cpu.cpu import CPU
from src.cpu.instruction_runner import Runner
from src.instruction.collection import InstructionCollection
from src.ppu.control import ppu_init


class Emulator():
    def __init__(self, cartridge_path):
        self.cpu = CPU()
        self.memory = None
        self.cart = None
        self.mapper = None
        self.instructions = None

        try:
            self.cart = Cartridge(cartridge_path)
            self.memory = Memory(self.cpu, self.cart)
            self.instructions = self.cart.get_prg_rom()

            if self.cart.get_mapper_type() == MapperType.NROM:
                self.mapper = NromMapper(self.cart)
            else:
                raise ValueError("Cartridge specifies a mapper type not supported yet")

            InstructionCollection.initialize()
            # PPU Render loop
            ppu_init.PPU_Runner_Initializer.init_ppu(self.cart.get_chr_rom(), self.memory.ppu_memory, self.memory.apu_memory.get_regs())
            Runner.run(self.instructions, self.cpu, self.memory)

        except ValueError as err:
            print("ERROR: ", end="")
            print(err.args)


def main(path="game/game.bin"):
    emulator = Emulator(path)


# ENTRY POINT
if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            main()
        elif len(sys.argv) == 2:
            main(sys.argv[1])
        else:
            Runner.log_as_nestest()
            main(sys.argv[1])
    except Exception as e:
        sys.exit(0)

