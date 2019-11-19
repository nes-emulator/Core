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

[Main Page](https://wiki.nesdev.com/w/index.php/APU)

[Registers](https://wiki.nesdev.com/w/index.php/APU_registers)

[Pulse](https://wiki.nesdev.com/w/index.php/APU_Pulse)

[Triangle](https://wiki.nesdev.com/w/index.php/APU_Triangle)

[Noise](https://wiki.nesdev.com/w/index.php/APU_Noise)

[DMC](https://wiki.nesdev.com/w/index.php/APU_DMC)

[Frame Counter](https://wiki.nesdev.com/w/index.php/APU_Frame_Counter)

[Length Counter](https://wiki.nesdev.com/w/index.php/APU_Length_Counter)

[Envelope](https://wiki.nesdev.com/w/index.php/APU_Envelope)

[Sweep](https://wiki.nesdev.com/w/index.php/APU_Sweep)

[Mixer](https://wiki.nesdev.com/w/index.php/APU_Mixer)

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

## PyPy + Pygame
- Download pypy
```console
wget https://bitbucket.org/pypy/pypy/downloads/pypy3.6-v7.2.0-linux64.tar.bz2
tar xf pypy3.6-v7.2.0-linux64.tar.bz2; rm pypy3.6-v7.2.0-linux64.tar.bz2
rm pypy3.6-v7.2.0-linux64.tar.bz2
```
- Install pygame build dependencies
```console
sudo apt-get install git python3-dev python3-setuptools python3-numpy python3-opengl \
    libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev \
    libsdl1.2-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev \
    libtiff5-dev libx11-6 libx11-dev fluid-soundfont-gm timgm6mb-soundfont \
    xfonts-base xfonts-100dpi xfonts-75dpi xfonts-cyrillic fontconfig fonts-freefont-ttf libfreetype6-dev
```

- rename pypy3.6-v7.2.0-linux64 folder to pypy

```console
mv pypy3.6-v7.2.0-linux64 pypy
```

- install pygame on pypy

```console
pypy/bin/pypy3 -m ensurepip
pypy/bin/pip install -U pip wheel
pypy/bin/pip install pygame  
```
- run using pypy

```console
 pypy/bin/pypy3 emulator.py game/game.bin
```

## Other tools
- https://wiki.nesdev.com/w/index.php/Tools

## Aplicando todos os testes do emulador
- `python3 -m unittest discover .`
