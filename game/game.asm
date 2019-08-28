;----------------------------------------------------------------
; constants
;----------------------------------------------------------------

    ONE = $01
    ZERO = $00

    FIRST_SPRITE_Y = $0200
    FIRST_SPRITE_TILE = $0201
    FIRST_SPRITE_CONTROL = $0202
    FIRST_SPRITE_X = $0203

    PRG_COUNT = 1 ; 1 = 16KB, 2 = 32KB
    MIRRORING = %0001 ; %0000 = horizontal, %0001 = vertical, %1000 = four-screen

    ; Include external constants

    .include "logic/logic_constants.asm"


;----------------------------------------------------------------
; variables
;----------------------------------------------------------------

   .enum $0000

   ; Variables for background
   tile        .dsb 1
   tile_count  .dsb 1
   attrLow     .dsb 1
   attrHigh    .dsb 1
   attrLow2    .dsb 1
   attrHigh2   .dsb 1
   aux         .dsb 4

   ;------------------------
   stkA .dsb 1; A swap variable, only to be used in stack operations
   ;------------------------

  .ende

  ;----------------------------------
  ; Logic Variables
  ;---------------------------------

  .enum $0300
      .include "logic/logic_variables.asm"
      .include "sound/sound_variables.asm"
      .include "graphics/graphic_variables.asm"
  .ende

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

logicMatrix:
    .include "logic/logic_mat.asm"

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
