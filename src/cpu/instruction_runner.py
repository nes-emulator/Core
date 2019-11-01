from src.instruction.collection import InstructionCollection
from src.register.statusregister import StatusRegister
from .logger import Logger


class InterruptVectorAddressResolver:
    @staticmethod
    def get_reset_address(mem):
        reset_bytes = [mem.retrieve_content(0xFFFC), mem.retrieve_content(0xFFFD)]
        return int.from_bytes(reset_bytes, byteorder='little')

    @staticmethod
    def get_nmi_address(mem):
        nmi_bytes = [mem.retrieve_content(0xFFFA), mem.retrieve_content(0xFFFB)]
        return int.from_bytes(nmi_bytes, byteorder='little')


class Runner:
    PRG_ROM_START = 0
    LOGGER_ACTIVE = False
    NESTEST = False
    CPU_FREQUENCY_HZ = 1789773

    @staticmethod
    def run(prg_rom, cpu, mem):
        reset_pos = InterruptVectorAddressResolver.get_reset_address(mem)

        if not Runner.NESTEST:
            cpu.state.pc.set_value(reset_pos)
        else:
            cpu.state.pc.set_value(0xc000)
            cpu.state.status = StatusRegister(36)

        while True:
            params = []

            if Runner.NESTEST:
                Logger.log_nestest(cpu)

            opcode = mem.retrieve_content(cpu.state.pc.get_value())
            ins = InstructionCollection.get_instruction(opcode)
            for _ in range(getattr(ins, 'parameter_length', 0)):
                cpu.state.pc.inc()
                params.append(mem.retrieve_content(cpu.state.pc.get_value()))

            cpu.state.pc.inc()
            manipulated_mem_addr = ins.execute(memory=mem, cpu=cpu, params=params)

            if Runner.LOGGER_ACTIVE and not Runner.NESTEST:
                Logger.log_reg_status(cpu.state, cpu.state.pc.get_value())
                if not manipulated_mem_addr is None:
                    Logger.log_mem_manipulation(mem, manipulated_mem_addr)
                Logger.next_log_line()

            cpu.cycles += ins.get_cycles()

            if Runner.should_redirect_to_nmi(cpu, mem):
                # notify PPU
                # status = memory.ppu_memory.regs[2] | 0b10000000     # set NMI bit
                # memory.ppu_memory.regs[2] = status
                # memory.set_content(PPUSTATUS.BASE_ADDR, status)

                # run NMI code
                cpu.cycles = 0
                mem.stack.push_pc()
                mem.stack.push_val(cpu.state.status.to_val())
                nmi_address = InterruptVectorAddressResolver.get_nmi_address(mem)
                cpu.state.pc.set_value(nmi_address)

    @classmethod
    def activate_log(cls):
        Runner.LOGGER_ACTIVE = True

    @classmethod
    def deactivate_log(cls):
        Runner.LOGGER_ACTIVE = False

    @classmethod
    def log_as_nestest(cls):
        Runner.NESTEST = True

    @staticmethod
    def should_redirect_to_nmi(cpu, memory):
        is_nmi_enabled = memory.ppu_memory.regs[0] & 0b10000000

        if not is_nmi_enabled:
            return False

        # TODO better way of deciding to change to NMI
        if cpu.cycles / 4000 > 1:
            return True

        return False
