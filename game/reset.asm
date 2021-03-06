;;;;; RESET SETUP ;;;;;

  SEI          ; disable IRQs
  CLD          ; disable decimal mode
  LDX #$40
  STX $4017    ; disable APU frame IRQ
  LDX #$FF
  TXS          ; Set up stack
  INX          ; now X = 0
  STX $2000    ; disable NMI
  STX $2001    ; disable rendering
  STX $4010    ; disable DMC IRQs

vblankwait1:       ; First wait for vblank to make sure PPU is ready
  BIT $2002
  BPL vblankwait1

clrmem:
  LDA #$00
  STA $0000, x
  STA $0100, x
  STA $0300, x
  STA $0400, x
  STA $0500, x
  STA $0600, x
  STA $0700, x
  LDA #$FE
  STA $0200, x
  INX
  BNE clrmem

vblankwait2:      ; Second wait for vblank, PPU is ready after this
  BIT $2002
  BPL vblankwait2


LoadPalettes:
  LDA $2002             ; read PPU status to reset the high/low latch
  LDA #$3F
  STA $2006             ; write the high byte of $3F00 address
  LDA #$00
  STA $2006             ; write the low byte of $3F00 address
  LDX #$00              ; start out at 0
LoadPalettesLoop:
  LDA palette, x        ; load data from address (palette + the value in x)
                          ; 1st time through loop it will load palette+0
                          ; 2nd time through loop it will load palette+1
                          ; 3rd time through loop it will load palette+2
                          ; etc
  STA $2007             ; write to PPU
  INX                   ; X = X + 1
  CPX #$1E              ; Compare X to hex $10, decimal 16 - copying 16 bytes = 4 sprites
  BNE LoadPalettesLoop  ; Branch to LoadPalettesLoop if compare was Not Equal to zero
                        ; if compare was equal to 32, keep going down



LoadSprites:
  LDX #$00              ; start at 0
LoadSpritesLoop:
  LDA sprites, x        ; load data from address (sprites +  x)
  STA $0200, x          ; store into RAM address ($0200 + x)
  INX                   ; X = X + 1
  CPX #$20              ;
  BNE LoadSpritesLoop   ; Branch to LoadSpritesLoop if compare was Not Equal to zero
                        ; if compare was equal to 16, keep going down

  LDX #ZERO             ; start out at 0
  STA control_sprite

  JSR LoadBackground    ; Load background function

  ; First reset bomberman position on screen
  LDA #$03
  STA bomberX
  STA bomberY
  JSR MoveBomberman

  LDA #%00011110   ; enable sprites, enable background, no clipping on left side
  STA $2001

  LDA #$00         ; No background scrolling
  STA $2006
  STA $2006
  STA $2005
  STA $2005

  LDA #0
  STA BomberDeathDelay
  LDA #1
  STA bomberState

; ;-----------------------------------------
; ; Initializes mob position
; ;-----------------------------------------
  LDA #11
  STA mobX
  LDA #10
  STA mobY           ; First reset bomberman position on screen
  JSR MoveMobSprites

  ; ; Initializes Mob delay counter
  LDA #0
  STA mobMoveCounter
  ;
  ; ; Sets Mob state
  LDA #1
  STA mobIsAlive
  LDA #RIGHT_DIRECTION
  STA mobDirection

  LDA #0
  STA DelayCounter
  JSR sound_init    ; APU setup

  LDA #%10010000   ; enable NMI, sprites from Pattern Table 0, background from Pattern Table 1
  STA $2000

Forever:
  JMP Forever     ;jump back to Forever, infinite loop
