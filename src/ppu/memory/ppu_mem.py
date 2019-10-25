class PPUMemory:

    UNSIGNED_BYTE_TYPE = 'B'

    def __init__(self):
        self.memory = array(PPUMemory.UNSIGNED_BYTE_TYPE, (0,) * 16384)
        self.oam = array(PPUMemory.UNSIGNED_BYTE_TYPE, (0,) * 256)

    def get_content(self):
        pass

    def set_content(self, addr):
        pass
