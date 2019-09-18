"""there are 11 addressing methods in the NES instructions
the respective addressing class should be passed to the Instruction during instantiation,
so it will become able to extract the parameters.

the following addressing classes are implemented in the order described in:

 reference : http://nesdev.com/6502.txt
"""

from src.util.util import make_16b_binary, add_binary
from src.memory.memory import Memory


class CalculateAddress:
    @classmethod
    def calculate_unified_parameter(cls, params, cpu, mem):
        pass

    # always return the
    @classmethod
    def retrieve_address_data(cls, mem, address):
        return mem.retrieve_content(address)


class BaseAddr(CalculateAddress):
    # addressing arguments - length
    parameter_length = 0  # in bytes

    @classmethod
    def get_parameter_length(cls):
        return cls.parameter_length

    @classmethod
    def get_offset(cls, cpu):
        pass


class ImmediateAddr(BaseAddr):  # 1
    parameter_length = 1

    # reuturns the parameter value (imediate)
    @classmethod
    def calculate_unified_parameter(cls, params, cpu, mem):
        return params[0]

    @classmethod
    def retrieve_address_data(cls, mem, value):
        return value


class ZeroPageAddr(BaseAddr):  # 2
    parameter_length = 1

    # returns the parameter value  (1 byte)
    @classmethod
    def calculate_unified_parameter(cls, params, cpu, mem):
        return params[0]


class AbsoluteAddr(BaseAddr):  # 3
    parameter_length = 2  # absolute address = 1 word

    # first param = low byte, second = high byte
    # returns the parameter value  (2 bytes)
    @classmethod
    # Absolute memory indexing
    # return the memory address of the absolute address
    def calculate_unified_parameter(cls, params, cpu, mem):
        return make_16b_binary(params[1], params[0])  # low byte is stored first

    pass


class ImpliedAddr(BaseAddr):  # 4
    # return nothing, eg TAX
    parameter_length = 0
    pass


class AccumulatorAddr(BaseAddr):  # 5
    parameter_length = 0

    # return the value of the accumulator reg
    @classmethod
    def calculate_unified_parameter(cls, params, cpu, mem):
        return cpu.state.a


class ZeroPgDirectIndexedRegXAddr(BaseAddr):  # 7.1
    parameter_length = 1

    # returns the value of the X addres + zero page parameter
    @classmethod
    def calculate_unified_parameter(cls, params, cpu, mem):
        address = params[0]
        return address + cpu.state.x


class ZeroPgDirectIndexedRegYAddr(BaseAddr):  # 7.2
    parameter_length = 1

    # returns the value of the Y addres + zero page parameter
    @classmethod
    def calculate_unified_parameter(cls, params, cpu, mem):
        address = params[0]
        return address + cpu.state.y


class AbsDirectIndexedRegXAddr(BaseAddr):
    parameter_length = 2

    # the same as DirectIndexingAddr but use reg x offset
    @classmethod
    def calculate_unified_parameter(cls, params, cpu, mem):
        address = make_16b_binary(params[1], params[0])
        return address + cpu.state.x


class AbsDirectIndexedRegYAddr(BaseAddr):
    parameter_length = 2

    # the same as DirectIndexingAddr but use reg y offset
    @classmethod
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

    @classmethod
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
        address, _ = add_binary(cpu.state.x, params[0], Memory.WORD_SIZE)
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


class RelativeIndexedAddr(BaseAddr):  # 11
    # BEQ +- 127
    parameter_length = 1
    #return the displacement offset
    @classmethod
    def calculate_unified_parameter(cls, params, cpu, mem):
        return params[0]  # branch offset
