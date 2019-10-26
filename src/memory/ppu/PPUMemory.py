from src.ppu.control.ppu_init import PPU_Runner_Initializer


class PPUMemory:
    PPU_MEM_SIZE = 16384  # 2kb ram
    PPU_OAM_SIZE = 256
    NUM_REGS = 8

    UNSIGNED_BYTE = 'B'

    def __init__(self):
        self.clear_memory()

    # TODO Init regs with power up state

    def clear_memory(self):
        self.memory = PPU_Runner_Initializer.mp_context.Array(PPUMemory.UNSIGNED_BYTE, (0,) * PPUMemory.PPU_MEM_SIZE)
        self.oam_memory = PPU_Runner_Initializer.mp_context.Array(PPUMemory.UNSIGNED_BYTE, (0,) * PPUMemory.PPU_OAM_SIZE)
        self.regs = PPU_Runner_Initializer.mp_context.Array(PPUMemory.UNSIGNED_BYTE, (0,) * PPUMemory.NUM_REGS)

    def get_regs(self):
        return self.regs

    def get_val_oam(self, addr):
        return self.oam_memory[addr]

    def set_val_oam(self, addr, val):
        self.oam_memory[addr] = val

    def get_val_memory(self, addr):
        return self.memory[addr]

    def set_val_memory(self, addr, val):
        self.apply_ppu_mirroring(addr, val)
        self.memory[addr] = val

    def get_memory(self):
        return self.memory

    def get_oam(self):
        return self.oam_memory

    @staticmethod
    def solve_ppu_mirroring(addr):
        if 0x3000 <= addr <= 0x3EFF:
            return addr - 0x1000
        if 0x2000 <= addr <= 0x2EFF:
            return addr + 0x1000
        if 0x3F20 <= addr <= 0x3FFF:
            return addr - 0x20
        if 0x3F00 <= addr <= 0x3F1F:
            return addr + 0x20
        return None

    def apply_ppu_mirroring(self, addr, val):
        ppu_mirror = PPUMemory.solve_ppu_mirroring(addr)
        if ppu_mirror:
            self.memory[ppu_mirror] = val
