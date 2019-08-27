;;;;;;;;;;;;;;; NMI ;;;;;;;;;;;;;;;


;TODO handle death of bomber in NMI
; if bomberState = #DEAD
; controllers must be locked
; mobs and explosion should stop
; only a "Game sound" should play

;TODO handle different stages of brick explosion
;looking at "numberOfBricksExploding" , "explodingBricksXCoor" and "explodingBricksYCoor" all defined in logic.asm

PHA
TYA
PHA
TXA
PHA             ; Push all registers to stack

LDA #$00
STA $2003       ; set the low byte (00) of the RAM address
LDA #$02
STA $4014       ; set the high byte (02) of the RAM address, start the transfer

; tell both controllers to latch buttons
LatchController:
    LDA #$01
    STA $4016
    LDA #$00
    STA $4016

ReadController:
  LDX #$08
ReadControllerLoop:
  LDA $4016
  LSR A           ; bit0 -> Carry
  ROL buttons     ; bit0 <- Carry
  DEX
  BNE ReadControllerLoop

  ;bit:       7     6     5     4     3     2     1     0
  ;button:    A     B   select start  up   down  left right

; Enforces a delay of 30 frames in player movement
MoveDelayControl:
    LDA BomberMoveCounter
    CMP #0
    BNE UpdateMovementDelay

; We read only one movement per frame
Right:
    LDA buttons
    AND #%00000001
    BEQ Left
        JSR ResetBomberMovDelay
        LDA #RIGHT_MOVEMENT
        STA bomberMovDirection
        JSR MoveBomber_Logic
    JMP EndOfButtonMovement

Left:
    LDA buttons
    AND #%00000010
    BEQ Down
        JSR ResetBomberMovDelay
        LDA #LEFT_MOVEMENT
        STA bomberMovDirection
        JSR MoveBomber_Logic
    JMP EndOfButtonMovement

Down:
    LDA buttons
    AND #%00000100
    BEQ Up
        JSR ResetBomberMovDelay
        LDA #DOWN_MOVEMENT
        STA bomberMovDirection
        JSR MoveBomber_Logic
    JMP EndOfButtonMovement

Up:
    LDA buttons
    AND #%00001000
    BEQ EndOfButtonMovement
        JSR ResetBomberMovDelay
        LDA #UP_MOVEMENT
        STA bomberMovDirection
        JSR MoveBomber_Logic
    JMP EndOfButtonMovement

; if moveCounter > 0, decrements it
UpdateMovementDelay:
    DEC BomberMoveCounter
    JMP ReadBombSetup

EndOfButtonMovement:
ReadBombSetup:
    LDA buttons
    AND #%10000000          ; Read A button pressed
    BEQ EndReadBombSetup
        JSR placeBomb

EndReadBombSetup:

;;;;;;;;;;;;;;;;;; GAME STATE ;;;;;;;;;;;;;;;;;;

BombControl:
    LDA bombIsActive
    CMP #BOMB_DISABLED
    BEQ ExplosionState            ; Ignore control if there is no active bomb

BombTickControl:
    INC tickCounter
    LDA tickCounter
    CMP #30                 ; Reached full bomb tick cycle on #30
    BNE BombCounterControl
    LDA #$00
    STA tickCounter         ; Reset tick counter for next animation count
    LDA #1
    STA bombSFX             ; set Sound Engine flag
    JSR BombNextAnimationStage

BombCounterControl:
    INC bombCounter
    LDA bombCounter
    CMP #BOMB_BASE_TIMER
    BNE ExplosionState
    ; call explosion logic func, BOMB_BASE_TIMER = #120
    JSR bombExplosion
    ;
    LDA #1
    STA explosionSFX        ; set sound engine flag

ExplosionState:
    LDA ExplosionIsActive
    CMP #0
    BEQ next
        INC expCounter
        LDA expCounter
        CMP #60
        BNE MobControl
            ; render something
            LDA #0                  ; Deactivate explosion on screen
            STA ExplosionIsActive
			JSR RemoveExplosionRender

MobControl:
    LDA MobIsAlive
    CMP #0
    BEQ next
        INC mobMoveCounter
        LDA mobMoveCounter
        CMP #MOB_MOV_INTERVAL
        BNE next
            ; call mobWalk
            ; call mob render
            LDA #0
            STA mobMoveCounter       ; resets the counter

next:
playSoundFrame:
    JSR soundEngine

PLA
TAX
PLA
TAY
PLA                 ; Pull all registers from stack

RTI

; Resets the moveCounter whenever the player moves
ResetBomberMovDelay:
    LDA #10
    STA BomberMoveCounter
    RTS

;;;;;;;;;;;;;;; OLD NMI CODE BELOW

;
; ReadA:
;     LDA $4016       ; yer 1 - A
; 	AND #%00000001  ; only look at bit 0
; 	BEQ ReadADone   ; branch to ReadADone if button is NOT pressed (0)
; 		            ; add instructions here to do something when button IS pressed (1)
;     ; JSR EternalBeep
;     JSR TriangleOn
; ReadADone:          ; handling this button is done
;
; ReadB:
;     LDA $4016       ; yer 1 - B
;     AND #%00000001  ; only look at bit 0
;     BEQ ReadBDone   ; branch to ReadADone if button is NOT pressed (0)
; 	                ; add instructions here to do something when button IS pressed (1)
;     ; JSR ClearSQ1
;     JSR TriangleOff
; ReadBDone:          ; handling this button is done
;
;     ReadSelect:
; 	LDA $4016       ; yer 1 - Select
; 	AND #%00000001  ; only look at bit 0
; 	BEQ ReadSelectDone   ; branch to ReadADone if button is NOT pressed (0)
; 		        ; add instructions here to do something when button IS pressed (1)
;     ReadSelectDone:        ; handling this button is done
;
;     ReadStart:
; 	LDA $4016       ; yer 1 - Start
; 	AND #%00000001  ; only look at bit 0
; 	BEQ ReadStartDone   ; branch to ReadADone if button is NOT pressed (0)
; 		        ; add instructions here to do something when button IS pressed (1)
;     ReadStartDone:        ; handling this button is done
;
;     ReadUp:
; 	LDA $4016       ; player 1 - Start
; 	AND #%00000001  ; only look at bit 0
; 	BEQ ReadUpDone   ; branch to ReadADone if button is NOT pressed (0)
; 		        ; add instructions here to do something when button IS pressed (1)
;
; 	LDX #$01
; 	JSR MoveBombermanDirection
;
; 	LDX #ZERO              ; start at 0
;
; YUpMovementInBoundaries:
; 	LDA FIRST_SPRITE_Y,x
; 	SEC
; 	SBC #ONE
; 	JSR VerifyYUpWallBoundaries
; 	BEQ ReadUpDone
; 	INX
; 	INX
; 	INX
; 	INX
; 	CPX #LAST_SPRITE_END
; 	BNE YUpMovementInBoundaries
;
; 	LoadSpritesLoopUp:
; 	    LDA FIRST_SPRITE_Y,x       ; load sprite X position
; 	    SEC             ; make sure carry flag is set
; 	    SBC #ONE        ; A = A + 1
; 	    STA FIRST_SPRITE_Y,x       ; save sprite X position
;
; 	    INX
; 	    INX
; 	    INX
; 	    INX
;
; 	    CPX #LAST_SPRITE_END              ; Compare X to hex $10, decimal 32
; 	    BNE LoadSpritesLoopUp   ; Branch to LoadSpritesLoop if compare was Not Equal to zero
;
;
;
;
;     ReadUpDone:        ; handling this button is done
;
;
;     ReadDown:
; 	LDA $4016       ; player 1 - Start
; 	AND #%00000001  ; only look at bit 0
; 	BEQ ReadDownDone   ; branch to ReadADone if button is NOT pressed (0)
; 		        ; add instructions here to do something when button IS pressed (1
;
;
; 	LDX #$02
; 	JSR MoveBombermanDirection ; move down
;
; 	LDX #ZERO              ; start at 0
;
; 	YDownMovementInBoundaries:
; 	LDA FIRST_SPRITE_Y,x
; 	SEC
; 	SBC #ONE
; 	JSR VerifyYDownWallBoundaries
; 	BEQ ReadDownDone
; 	INX
; 	INX
; 	INX
; 	INX
; 	CPX #LAST_SPRITE_END
; 	BNE YDownMovementInBoundaries
;
; 	LoadSpritesLoopDown:
; 	    LDA FIRST_SPRITE_Y,x       ; load sprite X position
; 	    CLC             ; make sure carry flag is set
; 	    ADC #ONE        ; A = A + 1
; 	    STA FIRST_SPRITE_Y,x       ; save sprite X position
;
; 	    INX
; 	    INX
; 	    INX
; 	    INX
;
; 	    CPX #LAST_SPRITE_END              ; Compare X to hex $10, decimal 32
; 	    BNE LoadSpritesLoopDown   ; Branch to LoadSpritesLoop if compare was Not Equal to zero
;
;     ReadDownDone:        ; handling this button is done
;
;
;
;     ReadLeft:
; 	LDA $4016       ; player 1 - Start
; 	AND #%00000001  ; only look at bit 0
; 	BEQ ReadLeftDone   ; branch to ReadADone if button is NOT pressed (0)
; 		        ; add instructions here to do something when button IS pressed (1
;
; 	LDX #ZERO              ; start at 0
;
; XLeftMovementInBoundaries:
; 	LDA FIRST_SPRITE_X,x
; 	SEC
; 	SBC #ONE
; 	JSR VerifyXLeftWallBoundaries
; 	BEQ ReadLeftDone
; 	INX
; 	INX
; 	INX
; 	INX
; 	CPX #LAST_SPRITE_END
; 	BNE XLeftMovementInBoundaries
;
;
; 	LoadSpritesLoopLeft:
; 	    LDA FIRST_SPRITE_X,x       ; load sprite X position
; 	    SEC             ; make sure carry flag is set
; 	    SBC #ONE        ; A = A + 1
; 	    STA FIRST_SPRITE_X,x       ; save sprite X position
;
; 	    INX
; 	    INX
; 	    INX
; 	    INX
;
; 	    CPX #LAST_SPRITE_END              ; Compare X to hex $10, decimal 32
; 	    BNE LoadSpritesLoopLeft   ; Branch to LoadSpritesLoop if compare was Not Equal to zero
;
;     ReadLeftDone:        ; handling this button is done
;
;
;     ReadRight:
; 	LDA $4016       ; player 1 - B
; 	AND #%00000001  ; only look at bit 0
; 	BEQ ReadRightDone   ; branch to ReadBDone if button is NOT pressed (0)
; 		        ; add instructions here to do something when button IS pressed (1)
;
; 	LDX #ZERO              ; start at 0
;
; 	XRightMovementInBoundaries:
; 	LDA FIRST_SPRITE_X,x
; 	SEC
; 	SBC #ONE
; 	LDY FIRST_SPRITE_Y,x
; 	JSR VerifyXRightWallBoundaries
; 	BEQ ReadRightDone
; 	INX
; 	INX
; 	INX
; 	INX
; 	CPX #LAST_SPRITE_END
; 	BNE XRightMovementInBoundaries
;
; 	LoadSpritesLoopRight:
; 	    LDA FIRST_SPRITE_X,x       ; load sprite X position
; 	    CLC               ; make sure carry flag is set
; 	    ADC #ONE          ; A = A + 1
; 	    STA FIRST_SPRITE_X,x       ; save sprite X position
;
; 	    INX
; 	    INX
; 	    INX
; 	    INX
;
; 	    CPX #LAST_SPRITE_END              ; Compare X to hex $10, decimal 32
; 	    BNE LoadSpritesLoopRight   ; Branch to LoadSpritesLoop if compare was Not Equal to zero
;
;     ReadRightDone:        ; handling this button is done
;
;     RTI             ; return from interrupt
;
;
; ;parameter A  = sprite primary verification position (x or Y)
; ;Y = Sprite secundary verification (x or Y)
; VerifyXRightWallBoundaries:
;
;
;
;
;
;   CLC
;   SEC
;   CMP #RIGHT_LIMIT
;   BEQ endOfXRightVerification
;   ;Brick Verification
;   ;Verify Brick limits
;   ;first of all i will check which brick is still present
;
;   ;Inner Wall Verification
;   ;if he is nning move to the right, i have to verify possible shock with all left corners
;   ;of the inner walls
;
; ;   TAY
; ;   LDA #LEFT_LIMIT
; ;   JSR InnerWallsVerification
; ;   BNE endOfXRightVerification
;
; ;   PLY
; ;
;
; ;   LDA #TOP_LIMIT
; ;   JSR InnerWallsVerification
;
;
;   endOfXRightVerification:
; 	PLY
; 	PLX
;
;   	RTS
;
; VerifyXLeftWallBoundaries:
;   CLC
;   SEC
;   CMP #LEFT_LIMIT
;   BEQ endOfXLeftVerification
;   ;Verify Brick limits
;   :endOfXLeftVerification
;   RTS
;
; VerifyYUpWallBoundaries:
;   CLC
;   SEC
;   CMP #TOP_LIMIT
;   BEQ endOfYUpVerification
;   ;Verify Brick limits
;   endOfYUpVerification:
;   RTS
;
; VerifyYDownWallBoundaries:
;   CLC
;   SEC
;   CMP #BOT_LIMIT
;   BEQ endOfYDownVerification
;   ;Verify Brick limits
;   endOfYDownVerification:
;   RTS

;A will store the bitset
;X will store the number of the brick being processed
;requiredBrick is the parameter, a global variable declared in gamw.asm
;this function will return 0 in flag if the brick is present , otherwise it will return -1 in C
;   brickIsPresent:
; 	LDX #$00
; 	LDA activeBricks
; 	brickStatusLoop:
; 		LSR A
; 		INX
; 		BEQ currentBrickPresent ; the current brick is present

; 		;the required brick isnt present
; 		CPX requiredBrick
; 		BEQ endOfBrickVerification
; 		JMP brickStatusLoop

; 		currentBrickPresent:
; 		CPX requiredBrick
; 		BEQ endOfBrickVerificationWithFlag:


; 	endOfBrickVerification:
; 		LDA #$1
; 		CMP #$2
; 		RTS
; 	endOfBrickVerificationWithFlag:
; 		RTS

; ;Y = coordinate Postion Y Or Position X
; ;A = Boundary Position (top or Left)
; ; Return in Carry = 0 if the colision in this axis willl happen

; ;   InnerWallsVerification:
; ;
; ;
; ;
; ; 	InnerWallInnerVerificationLoop:
; ; 		CLC
; ; 		ADC #INNER_WALL_SIZE
; ; 		ADC #INNER_WALL_SIZE
; ; 		STA currentWallComparison
; ; 		CPY currentWallComparison
; ; 		BEQ EndOfVerification
; ; 		INX
; ; 		CPX #$3 ; change INNER_WALL_LINES later
; ; 		BNE InnerWallInnerVerificationLoop

; ; 	EndOfVerification:
; ; 		PLY
; ; 		PLX
; ;
; ; 		RTS
