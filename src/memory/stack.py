from src.cpu.cpu import state
from src.register import *
from src.register import statusregister
from src.util.util import apply_higher_byte_mask, apply_lower_byte_mask, make_16b_binary


class Stack:
    # descending stack
    START_ADDR = 0x1FF
    END_ADDR = 0x100

    def pop_pc(self):
        low_byte = self.pop_val()
        high_byte = self.pop_val()
        self.state.pc.set_value(make_16b_binary(high_byte, low_byte))

    def push_pc(self):
        pc_low_byte = apply_lower_byte_mask(self.state.pc.get_value())
        pc_high_byte = apply_higher_byte_mask(self.state.pc.get_value())
        self.push_val(pc_high_byte)
        self.push_val(pc_low_byte)

    def __init__(self, memory, cpu_state):
        self.memory = memory
        self.state = cpu_state
        self.set_top(Stack.START_ADDR)

    def pop_val(self):
        if self.empty_stk():
            pass
            # raise ("stack underflow")
        self.set_top(self.get_top() + 1)
        return self.memory.retrieve_content(self.get_top())

    def push_regs(self):
        self.push_val(self.state.x.get_value())
        self.push_val(self.state.y.get_value())
        self.push_pc(self.state.pc.get_value())
        self.push_val(self.state.status.to_val())

    # x
    # y
    # pc
    # status
    # save state
    def pop_regs(self):
        self.state.status = statusregister.StatusRegister(self.pop_val())
        self.pop_pc()
        self.state.y.set_value(self.pop_val())
        self.state.x.set_value(self.pop_val())

    # x
    # y
    # pc
    # status
    def push_val(self, val):

        if self.full_stk():
            pass
            # raise ("stack overflow")
        self.memory.set_content(self.get_top(), val)
        self.set_top(self.get_top() - 1)  # points to a empty pos

    # retrieve state

    def empty_stk(self):
        return self.get_top() == Stack.START_ADDR

    def full_stk(self):
        return self.get_top() == Stack.END_ADDR

    def get_top(self):
        return self.state.sp.get_value()

    def set_top(self, val):
        self.state.sp.set_value(val)
