from src.instruction.collection import InstructionCollection
from src.instruction.addressing import *


class Runner:
    PRG_ROM_START = 0  # fix

    @staticmethod
    def run(prg_rom, cpu, mem):
        cpu.state.pc = Runner.PRG_ROM_START
        while cpu.state.pc < len(prg_rom):
            # TODO regulate stall
            params = []
            ins = InstructionCollection.get_instruction(prg_rom[cpu.state.pc])
            for _ in range(ins.addressing.parameter_length):
                cpu.state.pc += 1
                params.append(prg_rom[cpu.state.pc])
            generic_param = ins.addressing.calculate_unified_parameter(params, cpu, mem)
            cpu.state.pc += 1
            ins.execute(memory=mem, cpu=cpu, param=generic_param)
