
;-----------------------------------------------------------------
; LoadBackground Main function
;-----------------------------------------------------------------

LoadBackground:
  LDA #$04
  STA tile_count        ; First reset tile count
  LDA $2002             ; read PPU status to reset the high/low latch
  LDA #$20
  STA $2006             ; write the high byte of $2000 address
  LDA #$00
  STA $2006             ; write the low byte of $2000 address
  LDX #$00              ; start out at 0
LoadBackgroundStart:
  LDY #$00              ; Redo stuff loop
LoadBackgroundLoop:
  LDA matrix, x
  STA tile              ; Write tile on PPU
  jsr ExtractDataFromTile

  INX
  CPX #$3C              ; Until end of background
  BEQ LoadAttribute     ; End of loop

  INY
  CPY #$04              ; Continue loop until it is time to repeat
  BNE LoadBackgroundLoop

LoadBackgroundRedo:
  TXA
  SEC
  SBC #$04              ; Return X value to start of background line
  TAX
  LDY #$00              ; Reset Y to count line one more time
LoadBackgroundRedoLoop:
  LDA matrix, x
  STA tile              ; Write redo tile on PPU
  jsr ExtractDataFromTile

  INX
  INY
  CPY #$04              ; Continue counting on Y to stop redo
  BEQ LoadBackgroundStart
  JMP LoadBackgroundRedoLoop

LoadAttribute:
  LDA #$04
  STA tile_count        ; Count of how many attributes until skip line
  LDA $2002             ; read PPU status to reset the high/low latch
  LDA #$23
  STA $2006             ; write the high byte of $23C0 address
  LDA #$C0
  STA $2006             ; write the low byte of $23C0 address
  LDX #$00              ; start out at 0
LoadAttributeLoop:
  LDA #%11111111
  STA $2007

  INX
  CPX #$08              ; Top space of screen with default attributes
  BNE LoadAttributeLoop

  LDX #$08              ; Reset X for matrix loop
LoadMatrixAttributesLoop:
  LDA #$00
  STA attrLow
  STA attrHigh          ; Reset variables

  LDA matrix, x
  AND #%11110000        ; Mask for get first attribute
  STA aux
  JSR LoadTileHighAttribute

  TXA
  TAY                   ; Copy Y to X

  INY                   ; Retrieve same info from line below
  INY
  INY
  INY                   ; Move Y to next line

  LDA matrix, y
  AND #%11110000        ; Get formated to wwzz0000
  STA aux
  JSR LoadTileLowAttribute

  LDA attrHigh
  ORA attrHigh2         ; Final form of wwzzxxyy for attribute
  STA $2007             ; Write attribute to PPU

  ; Start of second line for attribute table

  LDA matrix, x
  AND #%00001111        ; Mask for get other attributes
  ASL A
  ASL A
  ASL A
  ASL A
  CLC                   ; Format xxxx0000

  STA aux               ; Same logic to second high part
  JSR LoadTileHighAttribute

  TXA
  TAY                   ; Copy Y to X

  INY                   ; Retrieve same info from line below
  INY
  INY
  INY                   ; Move Y to next line

  LDA matrix, y
  AND #%00001111        ; Get formated to 0000xxx
  ASL A
  ASL A
  ASL A
  ASL A
  CLC                   ; Format xxxx0000

  STA aux               ; Extract low attribute second line
  JSR LoadTileLowAttribute

  LDA attrHigh
  ORA attrHigh2         ; Final form of wwzzxxyy for attribute
  STA $2007             ; Write attribute to PPU

  DEC tile_count
  LDA tile_count
  CMP #$00              ; Compare tile counters to know when to skip next line
  BEQ LoadMatrixAttributeSkipLine

  INX
  CPX #$3C              ; End of loop
  BCC LoadMatrixAttributesLoop

                        ; Jump to end if validation fails, ignore step below
  JMP LoadMatrixAttributesLoopEnd

LoadMatrixAttributeSkipLine:
  LDA #$04
  STA tile_count        ; Reset tile count for next skip line

  INX                   ; Move forward X count
  INX
  INX
  INX
  INX                   ; Then safely return to more loops

  JMP LoadMatrixAttributesLoop


LoadMatrixAttributesLoopEnd:
  RTS                   ; Return from function


;-----------------------------------------------------------------
; Auxiliar functions
;-----------------------------------------------------------------

ExtractDataFromTile:
  LDA tile

  AND #%11000000
  CMP #%00000000        ; 00 means grey tile
  BEQ GrayTile

  CMP #%01000000        ; 01 means green tile
  BEQ GreenTile
  JMP GrayTile          ; Default tile

GrayTile:
  LDA #$3a
  JMP ContinueExtractDataFromTile

GreenTile:
  LDA #$64
  JMP ContinueExtractDataFromTile

ContinueExtractDataFromTile:
  STA $2007             ; PPU Write background
  STA $2007             ; PPU Write background repeat

  CLC                   ; Move to right two times to get next tile
  ROL tile
  CLC
  ROL tile

  DEC tile_count        ; Continue the loop time_count times
  LDA tile_count
  CMP #$00
  BNE ExtractDataFromTile

  LDA #$04              ; Reset tile count on end of function
  STA tile_count
  RTS

LoadTileHighAttribute:
  LDA #$00
  STA attrLow
  STA attrHigh          ; Reset variables

  LDA aux               ; Entry point
  ASL A
  ROL attrHigh
  ASL A                 ; Getting first bits of attribute
  ROL attrHigh

  ASL A
  ROL attrLow
  ASL A                 ; Mask for second attribute
  ROL attrLow

  ASL attrLow           ; Reposition bits to 0000xx00
  ASL attrLow

  LDA attrHigh
  ORA attrLow
  STA attrHigh          ; Save in attrHigh 0000xxyy for attribute

  RTS

LoadTileLowAttribute:
  LDA #$00
  STA attrLow2
  STA attrHigh2         ; Reset variables

  LDA aux               ; Entry point zzww0000
  ASL A
  ROL attrHigh2
  ASL A                 ; Getting first bits of attribute
  ROL attrHigh2

  ASL A
  ROL attrLow2
  ASL A                 ; Mask for second attribute
  ROL attrLow2

  ASL attrLow2          ; Reposition bits to 0000ww00
  ASL attrLow2

  LDA attrHigh2
  ORA attrLow2
  STA attrHigh2         ; Save in attrHigh 0000wwzz for attribute

  ASL attrHigh2
  ASL attrHigh2
  ASL attrHigh2
  ASL attrHigh2         ; Move format to wwzz0000

  RTS
