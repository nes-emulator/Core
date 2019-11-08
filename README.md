# emulator

## Referência - Mês 1

[NerdyNights](http://nintendoage.com/forum/messageview.cfm?catid=22&threadid=7155): a series of NES programming lessons, starting from absolutely no knowledge.

[Easy 6502](https://skilldrick.github.io/easy6502/#intro): assembly tutorial.

## Referência - Mês 2

[NesDev 6502](http://nesdev.com/6502.txt): Registers, addressing modes, specification of some instructions.

[Instruction Set (NParker)](http://nparker.llx.com/a2/opcodes.html)

[Instruction Set (Masswerk)](https://www.masswerk.at/6502/6502_instruction_set.html#CMP)

[Formato dos logs de teste](https://github.com/AlissonLinhares/nesemu)

[NROM](https://wiki.nesdev.com/w/index.php/NROM)

[Mapper](https://wiki.nesdev.com/w/index.php/Mapper)

[Mirroring](https://wiki.nesdev.com/w/index.php/Mirroring)

[CPU memory map](https://wiki.nesdev.com/w/index.php/CPU_memory_map)

[Sample RAM map](https://wiki.nesdev.com/w/index.php/Sample_RAM_map): Explains pages.

[Page Cross](https://forums.nesdev.com/viewtopic.php?f=3&t=13936)

## Referências - Mês 03

[PPU Full Reference](http://wiki.nesdev.com/w/index.php/PPU)

## Referências - Mês 04

https://wiki.nesdev.com/w/index.php/APU_Mixer

https://www.reddit.com/r/esp8266/comments/9o8dtb/ive_emulated_the_8bit_nes_apu_registersdacs_on/

https://www.reddit.com/r/EmuDev/comments/ck5p3a/adding_apu_emulation_to_a_nes_emulator/

[Square Wave Example Pygame](https://gist.github.com/ohsqueezy/6540433)

## Referências instruções 6502
- http://www.6502.org/tutorials/6502opcodes.html
- http://www.obelisk.me.uk/6502/reference.html

## Repositório referências de código implementadas (NerdyNights)
- https://bitbucket.org/ddribin/nerdy-nights/src/default/

## Assembler NESASM para linux
- https://github.com/camsaul/nesasm

## Assembler ASM6F (oficial da disciplina)
- https://github.com/freem/asm6f

## Emulador FCEUX para linux
Usar o comando `nes` do linux para rodar visualmente os executáveis gerados
- `sudo apt-get install fceux`
- `nes file.nes`

## Emulador Mednafen (oficial da disciplina)
- `sudo apt-get install mednafen`

## Extensão do VSCode para 6502

- https://marketplace.visualstudio.com/items?itemName=EngineDesigns.retroassembler

## Other tools
- https://wiki.nesdev.com/w/index.php/Tools

## Aplicando todos os testes do emulador
- `python3 -m unittest discover .`
