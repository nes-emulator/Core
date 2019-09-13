"""there are 11 addressing methods in the NES instructions
the respective adressing class should be passed to the Instruction during instantiation, so it
 will become able to extract the parameters.

reference : http://nesdev.com/6502.txt
"""

from src.state import State
from src.memory import *
from src.util.util import make_16b_binary, add_binary


class BaseAddr:
    # adressing arguments - length
    parameter_length = 0  # in bytes

    @classmethod
    def get_parameter_length(cls):
        return cls.parameter_length

    @classmethod
    def calculate_unified_parameter(cls, params, cpu, mem):
        pass

    @classmethod
    def get_offset(cls, cpu):
        pass


class ImmediateAddr(BaseAddr):  # 1
    parameter_length = 1

    @classmethod
    def calculate_unified_parameter(cls, params):
        return params[0]


class ZeroPageAddr(BaseAddr):  # 2
    parameter_length = 1

    @classmethod
    def calculate_unified_parameter(cls, params, cpu, mem):
        mem.retrieve_content(params[0])


class AbsoluteAddr(BaseAddr):  # 3
    parameter_length = 2  # absolute address = 1 word

    @classmethod
    def calculate_unified_parameter(cls, params, cpu, mem):
        return make_16b_binary(params[1], params[0])  # low byte is stored first

    pass


class ImpliedAddr(BaseAddr):  # 4
    parameter_length = 0
    pass


class AccumulatorAddr(BaseAddr):  # 5
    parameter_length = 0

    @classmethod
    def get_value(cls, cpu):
        return cpu.state.a


class DirectIndexingAddr(BaseAddr):  # 6 zero page
    parameter_length = 2

    @classmethod
    def calculate_unified_parameter(cls, params, cpu, mem):
        address = make_16b_binary(params[1], params[0])
        return address


class ZeroPgDirectIndexedRegXAddr(BaseAddr):  # 7.1
    parameter_length = 1

    @classmethod
    def calculate_unified_parameter(cls, params, cpu, mem):
        address = params[0]
        return address + cpu.state.x


class ZeroPgDirectIndexedRegYAddr(BaseAddr):  # 7.2
    parameter_length = 1

    @classmethod
    def calculate_unified_parameter(cls, params, cpu, mem):
        address = params[0]
        return address + cpu.state.y


class AbsDirectIndexedRegXAddr(BaseAddr):
    parameter_length = 2

    @classmethod
    def calculate_unified_parameter(cls, params, cpu, mem):
        address = make_16b_binary(params[1], params[0])
        return address + cpu.state.x


class AbsDirectIndexedRegYAddr(BaseAddr):
    parameter_length = 2

    def calculate_unified_parameter(cls, params, cpu, mem):
        address = make_16b_binary(params[1], params[0])
        return address + cpu.state.y


class IndirectAddr(BaseAddr):  # 8

    """
  eg.  JMP ($215F)
  Assume the following
  byte    value
  $215F     $76
  $2160     $30
  This instruction takes the value of bytes $215F, $2160 and uses that as the
  address to jump to - i.e. $3076 (remember that addresses are stored with
  low byte first).
    """
    parameter_length = 2

    def calculate_unified_parameter(cls, params, cpu, mem):
        address = make_16b_binary(params[1], params[0])
        lowByte = mem.retrieve_content(address)
        highByte = mem.retrieve_content(address + 1)
        return make_16b_binary(highByte, lowByte)  # jmp address


# addition is used - i.e. the sum is always a zero-page address.
#    eg. FF + 2 = 0001 not 0101 as you might expect.
#    DON'T FORGET THIS WHEN EMULATING THIS MODE
class IndirectPreIndexedAddr(BaseAddr):  # 9 X
    parameter_length = 1

    @classmethod
    def calculate_unified_parameter(cls, params, cpu, mem):
        address, _ = add_binary(cpu.state.x, params[0])
        lowByte = mem.retrieve_content(address)
        highByte = mem.retrieve_content(address + 1)
        return make_16b_binary(highByte, lowByte)


class IndirectPostIndexedAddr(BaseAddr):  # 10
    parameter_length = 1

    @classmethod
    def calculate_unified_parameter(cls, params, cpu, mem):
        address = params[0]
        lowbyte = mem.retrieve_content(address)
        highbyte = mem.retrieve_content(address + 1)
        address = make_16b_binary(highbyte, lowbyte) + cpu.state.y
        return address


class RelativeAddr(BaseAddr):  # 11
    # BEQ +- 127
    parameter_length = 1

    @classmethod
    def calculate_unified_parameter(cls, params, cpu, mem):
        return params[0]  # branch offset