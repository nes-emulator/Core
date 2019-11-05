;;;;;;;;;;;;;;; NMI ;;;;;;;;;;;;;;;

;;;; Constants

MOB_MOV_DELAY = #30

; Push all registers to stack
PHA
TYA
PHA
TXA
PHA
JMP RAM

 ; Pull all registers from stack and RTI
returnFromNMI:
PLA
TAX
PLA
TAY
PLA
RTI

; RAM Setup
RAM:
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

;bit:       7     6     5     4     3     2     1     0
;button:    A     B   select start  up   down  left right
ReadController:
    LDX #$08
ReadControllerLoop:
    LDA $4016
    LSR A           ; bit0 -> Carry
    ROL buttons     ; bit0 <- Carry
    DEX
    BNE ReadControllerLoop


;;;; CHECK GAME STATE BEFORE MOVEMENT
DeathDelay:
    LDA bomberState
    CMP #0
    BNE MobControl
        LDA #0
        CMP BomberDeathDelay
        BNE DeathDelayCounter
        JSR RenderBombermanDeath
        ; checks a to finish the death animation
        DeathDelayCounter:
        INC BomberDeathDelay
        LDA BomberDeathDelay
        CMP #90
        ; BMI BombControl
        BMI ContinueDeath
            ; finish game here
            JMP Reset
            ContinueDeath:
                JMP playSoundFrame
            JMP returnFromNMI

;-------------------------------------------------------------------------------
; Start mob movement
;-------------------------------------------------------------------------------
MobControl:
    LDA mobIsAlive
    CMP #0
    BNE MoveDelayControl
    ; death of mob here
        LDA DelayCounter
        CMP #0
        BNE mobDeathCounter
            LDA #DOWN_DIRECTION
            STA bomberMovDirection
            JSR MoveBombermanDirection
            JSR RenderMobDeath
        mobDeathCounter:
        CMP #60
        BNE nextFrame
            JMP Reset

    nextFrame:
    INC DelayCounter
    JMP returnFromNMI

;-------------------------------------------------------------------------------
; End mob movement
;-------------------------------------------------------------------------------

;;;;;; READING CONTROLLERS

; Enforces a delay of 30 frames in player movement
MoveDelayControl:
    LDA BomberMoveCounter
    CMP #0
    BNE UpdateMovementDelay

; We read only one movement per frame
Right:
    LDA buttons
    AND #RIGHT_BUTTON
    BEQ Left
        JSR ResetBomberMovDelay
        LDA #RIGHT_DIRECTION
        STA bomberMovDirection
        JSR MoveBomberLogic
    JMP EndOfButtonMovement

Left:
    LDA buttons
    AND #LEFT_BUTTON
    BEQ Down
        JSR ResetBomberMovDelay
        LDA #LEFT_DIRECTION
        STA bomberMovDirection
        JSR MoveBomberLogic
    JMP EndOfButtonMovement

Down:
    LDA buttons
    AND #DOWN_BUTTON
    BEQ Up
        JSR ResetBomberMovDelay
        LDA #DOWN_DIRECTION
        STA bomberMovDirection
        JSR MoveBomberLogic
    JMP EndOfButtonMovement

Up:
    LDA buttons
    AND #UP_BUTTON
    BEQ EndOfButtonMovement
        JSR ResetBomberMovDelay
        LDA #UP_DIRECTION
        STA bomberMovDirection
        JSR MoveBomberLogic
    JMP EndOfButtonMovement

; if moveCounter > 0, decrements it
UpdateMovementDelay:
    DEC BomberMoveCounter
    JMP ReadBombSetup

EndOfButtonMovement:
ReadBombSetup:
    LDA buttons
    AND #A_BUTTON          ; Read A button pressed
    BEQ EndReadBombSetup
        JSR placeBomb

EndReadBombSetup:

;;;;;;;;;;;;;;;;;; GAME STATE ;;;;;;;;;;;;;;;;;;

MobAlive:
    LDA mobMoveCounter          ; Reads the current mob movement counter (used for delay in the movement)
    CMP #MOB_MOV_DELAY          ; Verifies if the last delay value was achieved
    BNE increaseMobMovementDelay  ; If not, increments the counter

    JSR MoveMobLogic
    JSR ResetMobMovDelay

    JMP BombControl

increaseMobMovementDelay:
    INC mobMoveCounter          ;  Increments mob counter movement

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
        JSR sound_bomb_tick     ; set Sound Engine flag
        JSR BombNextAnimationStage

BombCounterControl:
    INC bombCounter
    LDA bombCounter
    ; CMP #BOMB_BASE_TIMER
    CMP #120
    BNE ExplosionState
        ; call explosion logic func, BOMB_BASE_TIMER = #120
        JSR bombExplosion
        JSR sound_bomb_expl        ; set sound engine flag
        LDA #0
        STA bombCounter

ExplosionState:
    LDA ExplosionIsActive
    CMP #0
    BEQ next
        INC expCounter
        LDA expCounter
        CMP #60
        BNE next
            ; render something
            LDA #0                  ; Deactivate explosion on screen
            STA ExplosionIsActive
			JSR RemoveExplosionRender


next:
playSoundFrame:
    JSR sound_play_frame

JMP returnFromNMI


;-------------------------------------------------------------------------------
;-------------------------------------------------------------------------------
;- ResetMobMovDelay
;-   This subroutine clears the 'MobMoveCounter' variable (set to zeroto zero)
;-------------------------------------------------------------------------------
;-------------------------------------------------------------------------------
ResetMobMovDelay:
    PHA
    LDA #$0
    STA mobMoveCounter
    PLA
    RTS     ; End of 'ResetMobMovDelay' subroutine


; Resets the moveCounter whenever the player moves
ResetBomberMovDelay:
    LDA #BOMBER_MOVE_DELAY
    STA BomberMoveCounter
    RTS
