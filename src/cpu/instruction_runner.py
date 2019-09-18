from src.instruction.collection import InstructionCollection
from src.instruction.addressing import *
from .logger import Logger


class Runner:
    PRG_ROM_START = 0  # fix
    LOGGER_ACTIVE = True

    @staticmethod
    def run(prg_rom, cpu, mem):
        cpu.state.pc = Runner.PRG_ROM_START
        while cpu.state.pc < len(prg_rom):
            # TODO regulate stall
            params = []
            ins = InstructionCollection.get_instruction(prg_rom[cpu.state.pc])
            for _ in range(getattr(ins, 'parameter_length', 0)):
                cpu.state.pc += 1
                params.append(prg_rom[cpu.state.pc])

            cpu.state.pc += 1
            manipulated_mem_addr = ins.execute(memory=mem, cpu=cpu, params=params)
            if Runner.LOGGER_ACTIVE:
                Logger.log_reg_status(cpu.state)
                if not manipulated_mem_addr is None:
                    Logger.log_mem_manipulation(mem, manipulated_mem_addr)
                Logger.next_log_line()

    @classmethod
    def activate_log(cls):
        Runner.LOGGER_ACTIVE = False

    @classmethod
    def deactivate_log(cls):
        Runner.LOGGER_ACTIVE = True
