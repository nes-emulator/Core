import time
from time import sleep

from src.instruction.collection import InstructionCollection
from src.register.statusregister import StatusRegister
from .logger import Logger
from src.ppu.control.ppu_init import PPU_Runner_Initializer
from src.apu.play import APUPlayState

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
    NMI_INTERVAL = 100000
    CPU_FREQUENCY_HZ = 1789773
    CPU_PERIOD_S = 1 / CPU_FREQUENCY_HZ

    @staticmethod
    def run(prg_rom, cpu, mem):
        reset_pos = InterruptVectorAddressResolver.get_reset_address(mem)

        if not Runner.NESTEST:
            cpu.state.pc.set_value(reset_pos)
        else:
            cpu.state.pc.set_value(0xc000)
            cpu.state.status = StatusRegister(36)

        accumulated_delay = 0

        while PPU_Runner_Initializer.PPU_RUNNING.value:
            params = []

            if Runner.NESTEST:
                Logger.log_nestest(cpu)

            start_time = time.time()
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

            interval = time.time() - start_time
            cpu_period = Runner.CPU_PERIOD_S * ins.get_cycles()
            delay = cpu_period - interval

            cpu.cycles += ins.get_cycles()
            cpu.apu_cycles += ins.get_cycles() / 2
            cpu.ppu_cycles += 3 * ins.get_cycles()

            if delay > 0:
                accumulated_delay += delay
                if accumulated_delay >= 0.01:
                    sleep(accumulated_delay * 2)
                    accumulated_delay = 0

            cpu.ppu_cycles += 3 * ins.get_cycles()
            if Runner.should_redirect_to_nmi(cpu, mem):
                # notify PPU
                # status = memory.ppu_memory.regs[2] | 0b10000000     # set NMI bit
                # memory.ppu_memory.regs[2] = status
                # memory.set_content(PPUSTATUS.BASE_ADDR, status)
                # run NMI code
                cpu.ppu_cycles = 0
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
        if cpu.ppu_cycles > Runner.NMI_INTERVAL:
            status = memory.memory[0x2002]
            status = (status | 0b10000000)
            memory.memory[0x2002] = status

        is_nmi_enabled = memory.ppu_memory.regs[0] & 0b10000000
        return is_nmi_enabled and cpu.ppu_cycles > Runner.NMI_INTERVAL
