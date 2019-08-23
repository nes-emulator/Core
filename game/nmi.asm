
LDA #$00
STA $2003       ; set the low byte (00) of the RAM address
LDA #$02
STA $4014       ; set the high byte (02) of the RAM address, start the transfer


    LatchController:
	LDA #$01
	STA $4016
	LDA #$00
	STA $4016       ; tell both the controllers to latch buttons


ReadA:
    LDA $4016       ; player 1 - A
	AND #%00000001  ; only look at bit 0
	BEQ ReadADone   ; branch to ReadADone if button is NOT pressed (0)
		            ; add instructions here to do something when button IS pressed (1)
    ; JSR EternalBeep
    JSR TriangleOn
ReadADone:          ; handling this button is done

ReadB:
    LDA $4016       ; player 1 - B
    AND #%00000001  ; only look at bit 0
    BEQ ReadBDone   ; branch to ReadADone if button is NOT pressed (0)
	                ; add instructions here to do something when button IS pressed (1)
    ; JSR ClearSQ1
    JSR TriangleOff
ReadBDone:          ; handling this button is done

    ReadSelect:
	LDA $4016       ; player 1 - Select
	AND #%00000001  ; only look at bit 0
	BEQ ReadSelectDone   ; branch to ReadADone if button is NOT pressed (0)
		        ; add instructions here to do something when button IS pressed (1)
    ReadSelectDone:        ; handling this button is done

    ReadStart:
	LDA $4016       ; player 1 - Start
	AND #%00000001  ; only look at bit 0
	BEQ ReadStartDone   ; branch to ReadADone if button is NOT pressed (0)
		        ; add instructions here to do something when button IS pressed (1)
    ReadStartDone:        ; handling this button is done

    ReadUp:
	LDA $4016       ; player 1 - Start
	AND #%00000001  ; only look at bit 0
	BEQ ReadUpDone   ; branch to ReadADone if button is NOT pressed (0)
		        ; add instructions here to do something when button IS pressed (1)

	LDX #ZERO              ; start at 0

YUpMovementInBoundaries:
	LDA FIRST_SPRITE_Y,x
	SEC
	SBC #ONE
	JSR VerifyYUpWallBoundaries
	BEQ ReadUpDone
	INX
	INX
	INX
	INX
	CPX #LAST_SPRITE_END
	BNE YUpMovementInBoundaries
	
	LoadSpritesLoopUp:
	    LDA FIRST_SPRITE_Y,x       ; load sprite X position
	    SEC             ; make sure carry flag is set
	    SBC #ONE        ; A = A + 1
	    STA FIRST_SPRITE_Y,x       ; save sprite X position

	    INX
	    INX
	    INX
	    INX

	    CPX #LAST_SPRITE_END              ; Compare X to hex $10, decimal 32
	    BNE LoadSpritesLoopUp   ; Branch to LoadSpritesLoop if compare was Not Equal to zero


	

    ReadUpDone:        ; handling this button is done

	
    ReadDown:
	LDA $4016       ; player 1 - Start
	AND #%00000001  ; only look at bit 0
	BEQ ReadDownDone   ; branch to ReadADone if button is NOT pressed (0)
		        ; add instructions here to do something when button IS pressed (1

	LDX #ZERO              ; start at 0

	YDownMovementInBoundaries:
	LDA FIRST_SPRITE_Y,x
	SEC
	SBC #ONE
	JSR VerifyYDownWallBoundaries
	BEQ ReadDownDone
	INX
	INX
	INX
	INX
	CPX #LAST_SPRITE_END
	BNE YDownMovementInBoundaries

	LoadSpritesLoopDown:
	    LDA FIRST_SPRITE_Y,x       ; load sprite X position
	    CLC             ; make sure carry flag is set
	    ADC #ONE        ; A = A + 1
	    STA FIRST_SPRITE_Y,x       ; save sprite X position

	    INX
	    INX
	    INX
	    INX

	    CPX #LAST_SPRITE_END              ; Compare X to hex $10, decimal 32
	    BNE LoadSpritesLoopDown   ; Branch to LoadSpritesLoop if compare was Not Equal to zero

    ReadDownDone:        ; handling this button is done


	
    ReadLeft:
	LDA $4016       ; player 1 - Start
	AND #%00000001  ; only look at bit 0
	BEQ ReadLeftDone   ; branch to ReadADone if button is NOT pressed (0)
		        ; add instructions here to do something when button IS pressed (1

	LDX #ZERO              ; start at 0

XLeftMovementInBoundaries:
	LDA FIRST_SPRITE_X,x
	SEC
	SBC #ONE
	JSR VerifyXLeftWallBoundaries
	BEQ ReadLeftDone
	INX
	INX
	INX
	INX
	CPX #LAST_SPRITE_END
	BNE XLeftMovementInBoundaries


	LoadSpritesLoopLeft:
	    LDA FIRST_SPRITE_X,x       ; load sprite X position
	    SEC             ; make sure carry flag is set
	    SBC #ONE        ; A = A + 1
	    STA FIRST_SPRITE_X,x       ; save sprite X position

	    INX
	    INX
	    INX
	    INX

	    CPX #LAST_SPRITE_END              ; Compare X to hex $10, decimal 32
	    BNE LoadSpritesLoopLeft   ; Branch to LoadSpritesLoop if compare was Not Equal to zero

    ReadLeftDone:        ; handling this button is done


    ReadRight:
	LDA $4016       ; player 1 - B
	AND #%00000001  ; only look at bit 0
	BEQ ReadRightDone   ; branch to ReadBDone if button is NOT pressed (0)
		        ; add instructions here to do something when button IS pressed (1)

	LDX #ZERO              ; start at 0

	XRightMovementInBoundaries:
	LDA FIRST_SPRITE_X,x
	SEC
	SBC #ONE
	JSR VerifyXRightWallBoundaries
	BEQ ReadRightDone
	INX
	INX
	INX
	INX
	CPX #LAST_SPRITE_END
	BNE XRightMovementInBoundaries

	LoadSpritesLoopRight:
	    LDA FIRST_SPRITE_X,x       ; load sprite X position
	    CLC               ; make sure carry flag is set
	    ADC #ONE          ; A = A + 1
	    STA FIRST_SPRITE_X,x       ; save sprite X position

	    INX
	    INX
	    INX
	    INX

	    CPX #LAST_SPRITE_END              ; Compare X to hex $10, decimal 32
	    BNE LoadSpritesLoopRight   ; Branch to LoadSpritesLoop if compare was Not Equal to zero

    ReadRightDone:        ; handling this button is done

    RTI             ; return from interrupt


VerifyXRightWallBoundaries:
  CLC
  SEC
  CMP #RIGHT_LIMIT
  RTS

VerifyXLeftWallBoundaries:
  CLC
  SEC
  CMP #LEFT_LIMIT
  RTS

VerifyYUpWallBoundaries:
  CLC
  SEC
  CMP #TOP_LIMIT
  RTS

VerifyYDownWallBoundaries:
  CLC
  SEC
  CMP #BOT_LIMIT
  RTS