from src.state import State
from src.memory.memory import Memory


class Logger:
    SEPARATOR = "|"

    # if file is not provided the log will be printed in the standard output
    @classmethod
    def log_reg_status(cls, state, out_file=None):
        hex_regs = [" pc = {} ".format(hex(state.pc)), "a = {} ".format(state.a),
                    "x = {} ".format(state.x), "y = {} ".format(state.y),
                    "sp = {} ".format(state.sp)]

        output = Logger.SEPARATOR + Logger.SEPARATOR.join(hex_regs) + Logger.SEPARATOR

        flag_reg_out = Logger.SEPARATOR + " p[NV-BDIZC] = {} " + Logger.SEPARATOR
        flags_int = [int(state.status.negative), int(state.status.overflow),
                     int(state.status.brk), int(state.status.decimal),
                     int(state.status.interrupt), int(state.status.zero), int(state.status.carry)]

        flags_str = [str(f) for f in flags_int]

        flag_reg_out = flag_reg_out.format("".join(flags_str))

        output += flag_reg_out

        if out_file is not None:
            with open(out_file, "w+") as f:
                f.write(output)
        else:
            print(output, end='')

    @classmethod
    def next_log_line(cls, out_file=None):
        if out_file is not None:
            with open(out_file, "w+") as f:
                f.write("\n")
        else:
            print("")


@classmethod
# when two address are manipulated at the same instruction, should we print 2 mem logs ?
def log_mem_manipulation(cls, memory, addr, out_file):
    out_mem = " MEM[{}] = {} " + Logger.SEPARATOR
    out_mem = out_mem.format(hex(addr), hex(memory.retrieve_content(addr)))
    pass
