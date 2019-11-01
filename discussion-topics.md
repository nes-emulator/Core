

# PPUADDR

## 1

Access to PPUSCROLL and PPUADDR during screen refresh produces interesting raster effects;
the starting position of each scanline can be set to any pixel position in nametable memory.
For more information, see PPU scrolling and tokumaru's sample code on the BBS.[9]

## 2

Is this readable? What happens if you try to?

# PPUDATA

## 1

VRAM reading and writing shares the same internal address register that rendering uses.
So after loading data into video memory, the program should reload the scroll position afterwards
with PPUSCROLL writes in order to avoid wrong scrolling.