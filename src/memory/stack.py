from src.cpu.cpu import state
from src.register import statusregister


class Stack:
    # descending stack
    START_ADDR = 0x1FF
    END_ADDR = 0x100

    def __init__(self, memory, cpu_state):
        self.memory = memory
        self.state = cpu_state
        self.set_top(Stack.START_ADDR)

    def push_val(self, val):
        if self.full_stk():
            raise ("stack overflow")
        self.memory.set_content(self.get_top(), val)
        self.set_top(self.get_top() - 1)  # points to a empty pos

    def pop_val(self):
        if self.empty_stk():
            raise ("stack underflow")
        self.set_top(self.get_top() + 1)
        return self.memory.retrieve_content(self.get_top())

    # x
    # y
    # pc
    # status
    # save state
    def push_regs(self):
        self.push_val(self.state.x.get_value())
        self.push_val(self.state.y.get_value())
        self.push_val(self.state.pc.get_value())
        self.push_val(self.state.status.to_val())

    # x
    # y
    # pc
    # status
    # retrieve state
    def pop_regs(self):
        self.state.status = statusregister.StatusRegister(self.pop_val())
        self.state.pc.set_value(self.pop_val())
        self.state.y.set_value(self.pop_val())
        self.state.x.set_value(self.pop_val())

    def empty_stk(self):
        return self.top_addr == Stack.START_ADDR

    def full_stk(self):
        return self.top_addr == Stack.END_ADDR

    def get_top(self):
        return self.state.sp.get_value()

    def set_top(self, val):
        self.state.sp.set_value(val)
