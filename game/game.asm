;----------------------------------------------------------------
; constants
;----------------------------------------------------------------
;top = 0x30
; bot = 0xd6
;right = 0xCA

;useless after refactoring
TOP_LIMIT = $2D
BOT_LIMIT = $D7
RIGHT_LIMIT = $DA
LEFT_LIMIT = $0F



ONE = $01
FOUR = $04
ZERO = $00

FIRST_SPRITE_Y = $0200
FIRST_SPRITE_TILE = $0201
FIRST_SPRITE_CONTROL = $0202
FIRST_SPRITE_X = $0203

PRG_COUNT = 1 ; 1 = 16KB, 2 = 32KB
MIRRORING = %0001 ; %0000 = horizontal, %0001 = vertical, %1000 = four-screen

APUFLAGS = $4015

;----------------------------------------------------------------
; variables
;----------------------------------------------------------------

   .enum $0000

   ;NOTE: declare variables using the DSB and DSW directives, like this:

   tile        .dsb 1 ; Variables for background
   tile_count  .dsb 1
   attrLow     .dsb 1
   attrHigh    .dsb 1
   attrLow2    .dsb 1
   attrHigh2   .dsb 1
   aux         .dsb 1
   buttons     .dsb 1
   ;------------------------
   stkA .dsb 1; A swap variable, only yo be used in stack operations
   ;------------------------

  .ende


   ;NOTE: you can also split the variable declarations into individual pages, like this:

   ;.enum $0100
   ;.ende

   ;.enum $0200
   ;.ende


;----------------------------------------------------------------
; iNES header
;----------------------------------------------------------------

   .db "NES", $1a ;identification of the iNES header
   .db PRG_COUNT ;number of 16KB PRG-ROM pages
   .db $01 ;number of 8KB CHR-ROM pages
   .db $00|MIRRORING ;mapper 0 and mirroring
   .dsb 9, $00 ;clear the remaining bytes

;----------------------------------------------------------------
; program bank(s)
;----------------------------------------------------------------

   .base $10000-(PRG_COUNT*$4000)

; TODO: is it ok to just include here?

Logic:
    .include "logic/logic.asm"

Sound:
    .include "sound/engine.asm"

Graphics:
    .include "graphics/engine.asm"

;----------------------------------------------------------------
; RESET
;----------------------------------------------------------------


Reset:
    .include "reset.asm"


;----------------------------------------------------------------
; NMI
;----------------------------------------------------------------

NMI:
    .include "nmi.asm"


;-----------------------------------------------------------------
; Graphics functions
;-----------------------------------------------------------------

    .include "graphics/loadbackground.asm"

;----------------------------------------------------------------
; IRQ
;----------------------------------------------------------------

IRQ:    ;NOTE: IRQ code goes here


;----------------------------------------------------------------
; palette and sprites goes here
;----------------------------------------------------------------

    .org $E000

palette:
    .include "graphics/palette.asm"

sprites:
    .include "graphics/sprites.asm"

attribute:
    .include "graphics/attributes.asm"
    .include "graphics/matrix.asm"

;----------------------------------------------------------------
; interrupt vectors
;----------------------------------------------------------------

    .org $fffa

    .dw NMI
    .dw Reset
    .dw IRQ

;----------------------------------------------------------------
; CHR-ROM bank
;----------------------------------------------------------------

    .incbin "bomberman.chr"