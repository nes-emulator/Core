import multiprocessing as mp
from src.ppu.driver import ppu_main
from src.memory.ppu import PPUMemory
from src.ppu.pygame.controller import Controllers


class PPU_Runner_Initializer:
    #   mp.set_start_method('spawn')
    mp_context = mp
    PPU_RUNNING = mp.Value('B', 1, lock=False)  # Game starts with ppu running

    @classmethod
    def init_ppu(cls, chr_rom, ppu_mem: PPUMemory):
        ppu_process = mp.Process(target=ppu_main, args=(chr_rom, ppu_mem.get_regs(), ppu_mem.get_memory(),
                                                        ppu_mem.get_oam(), PPU_Runner_Initializer.PPU_RUNNING))
        ppu_process.start()

    @classmethod
    def expose_context(cls):
        return cls.mp_context
