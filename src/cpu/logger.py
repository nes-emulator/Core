from src.state import State
from src.memory.memory import Memory


class Logger:
    SEPARATOR = "|"

    # if file is not provided the log will be printed in the standard output
    @classmethod
    def log_reg_status(cls, state, out_file=None):
        hex_regs = [
            " pc = 0x{:04x} ".format(state.pc.get_value()),
            " a = 0x{:02x} ".format(state.a.get_value()),
            " x = 0x{:02x} ".format(state.x.get_value()),
            " y = 0x{:02x} ".format(state.y.get_value()),
            " sp = 0x{:04x} ".format(state.sp.get_value())
        ]

        output = Logger.SEPARATOR + Logger.SEPARATOR.join(hex_regs)

        flag_reg_out = Logger.SEPARATOR + " p[NV-BDIZC] = {} " + Logger.SEPARATOR
        flags_int = [int(state.status.negative), int(state.status.overflow),
                     int(state.status.unused), int(state.status.brk), int(state.status.decimal),
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

    # log change mem vals
    @classmethod
    def log_mem_manipulation(cls, mem, addr, out_file=None):
        out_mem = " MEM[{}] = {} " + Logger.SEPARATOR
        out_mem = out_mem.format(hex(addr), hex(mem.retrieve_content(addr)))
        if out_file is not None:
            with open(out_file, "w+") as f:
                f.write(out_mem)
        else:
            print(out_mem, end="")
