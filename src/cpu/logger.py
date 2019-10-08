from src.state import State
from src.memory.memory import Memory
from src.memory.stack import Stack


class Logger:
    SEPARATOR = "|"

    # if file is not provided the log will be printed in the standard output
    @classmethod
    def log_reg_status(cls, state, pc, out_file=None):
        hex_regs = [
            " pc = 0x{:04x} ".format(pc),
            " a = 0x{:02x} ".format(state.a.get_value()),
            " x = 0x{:02x} ".format(state.x.get_value()),
            " y = 0x{:02x} ".format(state.y.get_value()),
            " sp = 0x{:04x} ".format(state.sp.get_value() + Stack.BASE_ADDR)
        ]

        output = Logger.SEPARATOR + Logger.SEPARATOR.join(hex_regs)

        flag_reg_out = "".join([Logger.SEPARATOR, " p[NV-BDIZC] = {} ", Logger.SEPARATOR])
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
        out_mem = "".join([" MEM[0x{:04x}] = 0x{:02x} ", Logger.SEPARATOR])
        out_mem = out_mem.format(addr, mem.retrieve_content(addr))
        if out_file is not None:
            with open(out_file, "w+") as f:
                f.write(out_mem)
        else:
            print(out_mem, end="")

    @classmethod
    def log_nestest(cls, cpu):
        log_str = "".join(["".join(["PC:", str(cpu.state.pc.get_value()), " "]),
                           "".join(["A:", '{:02X}'.format(cpu.state.a.get_value()), " "]),
                           "".join(["X:", '{:02X}'.format(cpu.state.x.get_value()), " "]),
                           "".join(["Y:", '{:02X}'.format(cpu.state.y.get_value()), " "]),
                           "".join(["P:", '{:02X}'.format(cpu.state.status.to_val()), " "]),
                           "".join(["SP:", '{:02X}'.format(cpu.state.sp.get_value()), " "]),
                           "".join("CYC:", str(cpu.cycles))])
        print(log_str)
