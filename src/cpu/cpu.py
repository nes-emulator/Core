import src.state as state

class CPU():

    def __init__(self):
        self.state = state.State()
        self.cycles = 7
        self.ppu_cycles = 0