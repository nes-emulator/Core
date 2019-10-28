import multiprocessing as mp
from src.ppu.driver import ppu_main
from src.memory.ppu import PPUMemory
#from src.ppu.pygame.controller import Controllers

class PPU_Runner_Initializer:
    #   mp.set_start_method('spawn')
    mp_context = mp

    @classmethod
    def init_ppu(cls, ppu_mem: PPUMemory):
        ppu_process = mp.Process(target=ppu_main, args=(ppu_mem.get_regs(), ppu_mem.get_memory(),
        ppu_mem.get_oam(),))
        # ppu_process = mp.Process(target=ppu_main, args=(ppu_mem.get_regs(), ppu_mem.get_memory(),
        # ppu_mem.get_oam(),Controllers.ctrl1_btn_states, Controllers.ctrl2_btn_states),)
        ppu_process.start()

    @classmethod
    def expose_context(cls):
        return cls.mp_context
