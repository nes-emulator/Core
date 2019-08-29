;-----------------------------------------------------------------
;stack functions

;TODO: Move stack functions to game.asm
;you need to call these function before every function
;in which you dont want to preserve the state of the 3 registers

;-------------------------------------------------------------------------------------
;matrix access subroutines

;-------------------------------------------------------------------------------
;-------------------------------------------------------------------------------
;- AccessLogicMatrixNewCoordinate
;-   This subroutine converts the two dimentional index [characterNewY][characterNewX],
;-   into one unique index. This one unique index is stored in A register.
;-   The following formula is used to do this convertion:
;-
;-                   A = characterNewX + characterNewY * NUMBER_COLUMNS
;-
;-   Obs: this subroutine will dirt the A register
;-
;- Parameters:
;-   'characterNewX' memory variable must be set to the new character (either Bomber or Mob) X position
;-   'characterNewY' memory variable must be set to the new character (either Bomber or Mob) Y position
;-
;- Return:
;-    'A' register containing the one dimentional index
;-------------------------------------------------------------------------------
;-------------------------------------------------------------------------------
AccessLogicMatrixNewCoordinate:
    ;-------------------------------------------------------------------------------
    ; Push all registers (Y) to stack
    ;-------------------------------------------------------------------------------
    TYA
    PHA

    LDA #$0
    LDY characterNewY

    ; Sets A register to 'characterNewY' * NUMBER_COLUMNS
    AccessLogicMatrixNewCoordinateLoop:
        CPY #$0                                ; Verifies if the total number of adds was achieved
        BEQ AccessLogicMatrixNewCoordinateEnd  ; If achieved, stop the loop
        DEY                                    ; Otherwise, decrements the total number of remaining adds

        CLC
        ADC #NUMBER_COLUMNS                    ; Adds the total number of columns to A register

        JMP AccessLogicMatrixNewCoordinateLoop ; Continues with the addition loop

    AccessLogicMatrixNewCoordinateEnd:
        CLC
        ADC characterNewX          ; Adds the current new bomber column (X new position) to the A register

        ;-------------------------------------------------------------------------------
        ; Pull all registers (Y) from stack
        ;-------------------------------------------------------------------------------
        STA stkA    ; Uses stkA as a temporary variable to store current A register value

        PLA
        TAY

        LDA stkA    ; Recovers the previous A register value from stkA variable

        RTS  ; End of MoveBomberLogic subroutine



;-----------------------------------------------------------------------------------------------------------------
;matrix verification subroutines

;Parameters: A = memory address positioned to X,Y coordinate and ; characterNewX and characterNewY
;if true, cmp flag  = 0
;aux subroutine
coordinateIsWall:; joe was removed by joe, and it's in fact no longer needed
    ;--------------------------------------- push all
    STA stkA
    PHA
    TYA
    PHA
    TXA
    PHA
    LDA stkA
    ;---------------------------------------
    JSR coordinateIsBrick
    BEQ endOfIsWall
    JSR CoordinateIsBomb ; bombs are also walls; JOE CODE IS NOT COVERING THIS CASE
    BEQ endOfIsWall
    TAX
    LDA logicMatrix, x
    CMP #MAT_WALL
    endOfIsWall:
    ;---------------- Pull All
    PLA
    TAX
    PLA
    TAY
    PLA
    ;-------------------------
    RTS


;Parameters: A = memory address positioned to X,Y coordinate
;if true, cmp flag  = 0
;aux subroutine
coordinateIsBrick:; Joe removed this method but it's necessary
    ;--------------------------------------- push all
    STA stkA
    PHA
    TYA
    PHA
    TXA
    PHA
    LDA stkA
    ;---------------------------------------
    TAX
    LDA logicMatrix, x
    CMP #MAT_BRICK
    ;---------------- Pull All
    PLA
    TAX
    PLA
    TAY
    PLA
    ;-------------------------
    RTS

;Parameters: characterNewX and characterNewY
;if true, cmp flag  = 0
;aux subroutine
CoordinateIsBomb: ; joe dont implemented this routine in his code this should be reimplemented
    ;--------------------------------------- push all
    STA stkA
    PHA
    TYA
    PHA
    TXA
    PHA
    LDA stkA
    ;---------------------------------------
    LDA bombIsActive ; if bomb is not active, return
    CMP BOMB_ENABLED
    BNE EndOfCoordinateIsBomb ;not active
    LDA characterNewX
    CMP bombX
    BNE EndOfCoordinateIsBomb
    LDA characterNewY
    CMP bombY
    EndOfCoordinateIsBomb:
    ;---------------- Pull All
    PLA
    TAX
    PLA
    TAY
    PLA
    ;-------------------------
    RTS

;Parameters: characterNewX and characterNewY
;if true, cmp flag  = 0
;aux subroutine
CoordinateIsMob: ; Joe deleted this method, this method should be reimplemented
    ;--------------------------------------- push all

    ;---------------------------------------
    LDA characterNewX
    CMP mobX
    BNE EndOfCoordinateIsMob
    LDA characterNewY
    CMP mobY
    EndOfCoordinateIsMob:
    ;---------------- Pull All
    RTS

;Parameters: characterNewX and characterNewY
;if true, cmp flag  = 0
;aux subroutine
;this routine will make register "A" dirty
CoordinateIsBomber: ; this method was deleted by joe and should be reimplemented
    ;--------------------------------------- push all

    ;---------------------------------------
    LDA characterNewX
    CMP bomberX
    BNE EndOfCoordinateIsBomber
    LDA characterNewY
    CMP bomberY
    EndOfCoordinateIsBomber:
    ;---------------- Pull All
     RTS
    ;-------------------------

;----------------------------------------------------------------------------------------------------------------
;bomber MovementLogic

;-------------------------------------------------------------------------------
;-------------------------------------------------------------------------------
;- ValidNewCoordinates
;-   This subroutine verifies if the new coordinates given by characterNewY and characterNewX
;-   are valid coordinates. That is, if they do not belong to a MAT_BRICK, MAT_WALL
;-   (from the logic matrix) or have the same new coordinates as the activated BOMB.
;-   If it is neither MAT_WALL, MAT_BRICK or BOMB, then ZERO flag will be clear. Otherwise,
;-   it will be set.
;-
;-   Obs: this subroutine will dirt the A register
;-
;- Parameters:
;-   'characterNewX' memory variable must be set to the new character (either Bomber or Mob) X position
;-   'characterNewY' memory variable must be set to the new character (either Bomber or Mob) Y position
;-
;- Return:
;-   ZERO flag cleared if new coordinates are valid, otherwise setted if not valid
;-------------------------------------------------------------------------------
;-------------------------------------------------------------------------------
ValidNewCoordinates:
    ;-------------------------------------------------------------------------------
    ; Push all registers (Y) to stack
    ;-------------------------------------------------------------------------------
    TYA
    PHA

    ; Verifies if bomb is active
    LDA bombIsActive
    SEC
    SBC #BOMB_DISABLED
    BEQ VerifyLogicalMatrixCells

    ; Verifies if the bomb is not an obstacle to the character
    LDA characterNewX
    CMP bombX
    BNE VerifyLogicalMatrixCells ; As long the bombX != characterNewX, the bomb is not an obstacle

    LDA characterNewY
    CMP bombY
    BNE VerifyLogicalMatrixCells ; As long the bombY != characterNewY, the bomb is not an obstacle

    ; If reaches here, then both bombY == characterNewY and bombX == characterNewX, therefore here
    ; the #01 value will indicate that the bomb is an obstacle and therefore the character must not transpass
    LDA #01
    JMP ValidNewCoordinatesEnd

    VerifyLogicalMatrixCells:
        ; Gets the matrix coordinate in the format A = characterNewY * num_columns + characterNewX
        JSR AccessLogicMatrixNewCoordinate

        ; Verifies if coordinate is valid (the character can transpass)
        TAY
        LDA logicMatrix,y
        SEC
        SBC #MAT_PASS

    ValidNewCoordinatesEnd:
        ;-------------------------------------------------------------------------------
        ; Pull all registers (Y) from stack
        ;-------------------------------------------------------------------------------
        STA stkA    ; Uses stkA as a temporary variable to store current A register value

        PLA
        TAY

        LDA stkA    ; Recovers the previous A register value from stkA variable

        RTS ; End of MoveBomberLogic subroutine





MoveBomberLogic:
    ;-------------------------------------------------------------------------------
    ; Push all registers (A, Y and X) to stack
    ;-------------------------------------------------------------------------------
    PHA
    TYA
    PHA
    TXA
    PHA

    ; Sets the new Bomber Coordinates (X and Y)
    LDA bomberX
    STA characterNewX
    LDA bomberY
    STA characterNewY

    ;-------------------------------------------------------------------------------
    ; Start reading Left movement
    ;-------------------------------------------------------------------------------
    LeftMovement:
        ; Gets the current Bomber direction
        LDA bomberMovDirection

        CMP #LEFT_DIRECTION      ; Verifies if the LEFT direction was chosen
        BNE RightMovement       ; If not, goes and verifies the next direction

        DEC characterNewX

        ;JRS rotateBomberLeft (EDINHA)

        JMP EndOfMovementDirVerification
    ;-------------------------------------------------------------------------------
    ; Finish reading Left movement
    ;-------------------------------------------------------------------------------


    ;-------------------------------------------------------------------------------
    ; Start reading Right movement
    ;-------------------------------------------------------------------------------
    RightMovement:
        ; Gets the current Bomber direction
        LDA bomberMovDirection

        CMP #RIGHT_DIRECTION     ; Verifies if the RIGHT direction was chosen
        BNE DownMovement       ; If not, goes and verifies the next direction

        INC characterNewX

        ;JRS rotateBomberRight (EDINHA)

        JMP EndOfMovementDirVerification
    ;-------------------------------------------------------------------------------
    ; Finish reading Right movement
    ;-------------------------------------------------------------------------------


    ;-------------------------------------------------------------------------------
    ; Start reading Down movement
    ;-------------------------------------------------------------------------------
    DownMovement:
        ; Gets the current Bomber direction
        LDA bomberMovDirection

        CMP #DOWN_DIRECTION     ; Verifies if the DOWN direction was chosen
        BNE UpMovement         ; If not, goes and verifies the next direction

        INC characterNewY

        ;JRS rotateBomberDown (EDINHA)

        JMP EndOfMovementDirVerification
    ;-------------------------------------------------------------------------------
    ; Finish reading Down movement
    ;-------------------------------------------------------------------------------


    ;-------------------------------------------------------------------------------
    ; Start reading Up movement
    ;-------------------------------------------------------------------------------
    UpMovement:
        ; Gets the current Bomber direction
        LDA bomberMovDirection

        CMP #UP_DIRECTION                ; Verifies if the UP direction was chosen
        BNE EndOfBomberMovement         ; If not, an invalid movement argument was passed.
                                        ;    Then, just terminate this subroutine call

        DEC characterNewY

        ;JRS rotateBomberUp (EDINHA)
    ;-------------------------------------------------------------------------------
    ; Finish reading Down movement
    ;-------------------------------------------------------------------------------


    EndOfMovementDirVerification:
        ; Verifies if the new bomber position is a valid one

        JSR ValidNewCoordinates
        BNE EndOfBomberMovement

        LDA characterNewX
        STA bomberX         ; Updates the X bomber variable with the new valid bomber position
        LDA characterNewY
        STA bomberY         ; Updates the Y bomber variable with the new valid bomber position

        ;-----------------------------------------------------------------------
        ; Verifies if the new mob position coincides with the Bomber position
        ;-----------------------------------------------------------------------
        JSR IsBomberKilledByMob
        BNE PerformMovement     ; If not, just terminates the mob movement without doing anything

        ; Otherwise, the bomber is killed by the mob and the reset
        ; subroutine is called to reinitiallize the game
        LDA #0
        STA bomberState


        PerformMovement:
            JSR sound_step
            JSR MoveBomberman   ; Updates bomber sprites. This subroutine is located in 'graphics/engine.asm'
            JSR MoveBombermanDirection  ; Changes bomberman facing direction sprite

        JMP EndOfBomberMovement

    EndOfBomberMovement:

    ;-------------------------------------------------------------------------------
    ; Pull all registers (A, Y and X) from stack
    ;-------------------------------------------------------------------------------
    PLA
    TAX
    PLA
    TAY
    PLA

    RTS ; End of MoveBomberLogic subroutine



;-------------------------------------------------------------------------------
;-------------------------------------------------------------------------------
;- IsBomberKilledByMob
;-   This subroutine verifies if both the Mob positions (mobX and mobY) coincides with
;-   the both bomber position (bomberX and bomberY). If coincides, the ZERO flag will
;-   be setted. If not, the ZERO flag will be clear.
;-
;-   Obs: this subroutine will dirt the A register
;-
;- Return:
;-   ZERO flag setted if mob coordinates coincides with the bomber coordinates, otherwise cleared
;-------------------------------------------------------------------------------
;-------------------------------------------------------------------------------
IsBomberKilledByMob:
    LDA bomberX
    CMP mobX
    BNE IsBomberKilledByMobEnd

    LDA bomberY
    CMP mobY

    IsBomberKilledByMobEnd:
        RTS ; End of MoveBomberLogic subroutine





;tickCounter = 0
;bombIsActive = 1
;bombCounter = 0
;update bomb coordinate
;place the bomb in the current bomber coordinate position
placeBomb: ; this method wasn't implemented by joe
    ;--------------------------------------- push all
    STA stkA
    PHA
    TYA
    PHA
    TXA
    PHA
    LDA stkA
    ;---------------------------------------

    LDA ExplosionIsActive
    CMP #$01
    BEQ endOfPlaceBomb

    LDA bombIsActive
    CMP #BOMB_ENABLED
    BEQ endOfPlaceBomb ;if an active bomb already exists, terminate

    ;change bomb coordinate to bomberman coordinate
    LDA bomberX
    STA bombX
    LDA bomberY
    STA bombY

    JSR BombRender

    ;update flags
    LDA #BOMB_ENABLED
    STA bombIsActive
    LDA #0
    STA bombCounter
    STA tickCounter

    endOfPlaceBomb:
    ;---------------- Pull All
    PLA
    TAX
    PLA
    TAY
    PLA
    ;-------------------------
    RTS

; this method set the position of the aux index ing variables (characterNewX and characterNewY) to the bomb coordinate
setMatIndexToBomb:
    ;-------------------------------------------------------------------------------
    ; Push A register
    ;-------------------------------------------------------------------------------
    PHA ; store A value

    LDA bombX
    STA characterNewX
    LDA bombY
    STA characterNewY

    ;-------------------------------------------------------------------------------
    ; Pull A register
    ;-------------------------------------------------------------------------------

    PLA ; retrieve A value
    RTS ;


;   LDA #MAT_PASS
;   STA logicMatrix, x ; the position is no longer a logic wall, EDINHA's exploding brick animation will be called in NMI,
;   ;by inspecting numberOfBricksExploding
;   LDX numberOfBricksExploding
;   LDA characterNewX
;   STA explodingBricksXCoor, x
;   LDA characterNewY
;   STA explodingBricksYCoor, x
;   INX
;   STX numberOfBricksExploding

; X: matrix linear brick position
; characterNewX: X coordinate of the brick
; characterNewY: Y coordinate of the brick
;this method is only called in a controlled environment , so there is no need to preserve the registers
;using the stack.
;add the exploding brick to a "control array" of cordinates and change its cell to a PASSAGE in logic matrix
explodeLogicalBrick:
    LDA #MAT_PASS
    STA logicMatrix, x ; the position is no longer a logic wall, EDINHA's exploding brick animation will be called in NMI, by inspecting numberOfBricksExploding
    LDX numberOfBricksExploding
    LDA characterNewX
    STA explodingBricksXCoor, x
    LDA characterNewY
    STA explodingBricksYCoor, x
    INX
    STX numberOfBricksExploding
    RTS


;TODO: a refactor (function extraction) would be nice, in order to save space
;Flags to set:
;ExplosionIsActive  = 1
;expCounter = 0
;bombIsActive = 0
;render is only activated in the end of the method
;when the bomb explodes many things can occur:
;0) explosion can the lmited by walls
;1) bomber can die, bomberState = #Dead
;2) mob can die, mobIsAlive = #DEAD (Death is instant there is no delay between the explosion and its propagation)
;3) a brick can be destroyed, update brick position to MAT_PAS in logic matrix
;Output-> 4 flags indicating to the PPU logic if the explosion need to be rendered in the four adjacent squares (explosion boundaries variables)
;Output -> 2 arrays of "numberOfBricksExploding" bricks coordinates (explodingBricksXCoor, explodingBricksYCoor)
bombExplosion:
  ;--------------------------------------- push all
    STA stkA
    PHA
    TYA
    PHA
    TXA
    PHA
    LDA stkA
  ;---------------------------------------
  ;set explosion flags

  LDA #$00
  STA expCounter   ;reset explosion counter
  STA bombIsActive ; disable bomb
  STA bombCounter

  LDA #$01
  STA ExplosionIsActive ;activate explosion


  ;all sides of the explosion animation start Enabled, the explosion is only limited by walls
  LDA #AFFECTED
  STA expLeftCoor
  STA expRightCoor
  STA expUpCoor
  STA expDownCoor


  ;Verify all four adjacent squares individualy
   JSR setMatIndexToBomb

  ;RIGHT
;---------------------------------------
  INC characterNewX

  JSR AccessLogicMatrixNewCoordinate ;change A to
  JSR ValidNewCoordinates
  BEQ rightExpMobDeathVer ;if the coordinate affected is not a wall
  LDX #NOT_AFFECTED ;the right side wasn't affected by the explosion
  STX expRightCoor
  ;---------------------------------------------------------
  rightBrickExpVer:
  JSR coordinateIsBrick
  BNE rightExpMobDeathVer
  TAX ; X = cell offset
  JSR explodeLogicalBrick
 ;------------------------------------------------------------
  rightExpMobDeathVer:
    JSR CoordinateIsMob
    BNE bomberDeathRightExp
    ;JSR RenderMobDeath
    LDA #0
    STA mobIsAlive


  bomberDeathRightExp:
    JSR CoordinateIsBomber
    BNE checkLeftExplosionEffect

    LDA #0
    STA bomberState

    ;JMP endOfBombExplosionLogic ; THE GAME IS OVER, TERMINATE FUNC
 ;---------------------------------------------

 ;restore parameter coordinates


 ;LEFT
 ;----------------------------------------------------------------

  checkLeftExplosionEffect:
  JSR setMatIndexToBomb
  DEC characterNewX
  JSR AccessLogicMatrixNewCoordinate ;change A to matrixOffset
  JSR ValidNewCoordinates
  BEQ leftExpMobDeathVer ;if the coordinate affected is not a wall
  LDX #NOT_AFFECTED ;the right side wasn't affected by the explosion
  STX expLeftCoor
  ;---------------------------------------------------------
  leftBrickExpVer:
  JSR coordinateIsBrick
  BNE leftExpMobDeathVer
  TAX ; X = cell offset
  JSR explodeLogicalBrick
 ;------------------------------------------------------------
  leftExpMobDeathVer:
    JSR CoordinateIsMob
    BNE bomberDeathLeftExp
    ;JSR RenderMobDeath
    LDA #0
    STA mobIsAlive


  bomberDeathLeftExp:
    JSR CoordinateIsBomber
    BNE checkUpExplosionEffect
    LDA #0
    STA bomberState

   ; JMP endOfBombExplosionLogic ; THE GAME IS OVER, TERMINATE FUNC
 ;----------------------------------------------------------------

;restore parameter coordinates


 ;UP
 ;-------------------------------------------
  checkUpExplosionEffect:
    JSR setMatIndexToBomb
    DEC characterNewY
    JSR AccessLogicMatrixNewCoordinate ;change A to
    JSR ValidNewCoordinates
    BEQ UpExpMobDeathVer ;if the coordinate affected is not a wall
    LDX #NOT_AFFECTED ;the right side wasn't affected by the explosion
    STX expUpCoor
    ;---------------------------------------------------------
    UpBrickExpVer:
    JSR coordinateIsBrick
    BNE UpExpMobDeathVer
    TAX ; X = cell offset
    LDA #MAT_PASS
    JSR explodeLogicalBrick
    ;------------------------------------------------------------
    UpExpMobDeathVer:
        JSR CoordinateIsMob
        BNE bomberDeathUpExp
        ;JSR RenderMobDeath
        LDA #0
        STA mobIsAlive


    bomberDeathUpExp:
        JSR CoordinateIsBomber
        BNE checkDownExplosionEffect
        LDA #0
        STA bomberState

        ;JMP endOfBombExplosionLogic ; THE GAME IS OVER, TERMINATE FUNC
 ;--------------------------------------------

;restore parameter coordinates

 ;DOWN
 ;------------------------------------------
    checkDownExplosionEffect:
    JSR setMatIndexToBomb
    INC characterNewY
    JSR AccessLogicMatrixNewCoordinate ;change A to
    JSR ValidNewCoordinates
    BEQ DownExpMobDeathVer ;if the coordinate affected is not a wall
    LDX #NOT_AFFECTED ;the right side wasn't affected by the explosion
    STX expDownCoor
    ;---------------------------------------------------------
    DownBrickExpVer:
    JSR coordinateIsBrick
    BNE DownExpMobDeathVer
    TAX ; X = cell offset
    JSR explodeLogicalBrick
    ;------------------------------------------------------------
    DownExpMobDeathVer:
        JSR CoordinateIsMob
        BNE bomberDeathDownExp
        ;JSR RenderMobDeath
        LDA #0
        STA mobIsAlive


    bomberDeathDownExp:
        JSR CoordinateIsBomber
        BNE middleExplosionEffect
        LDA #0
        STA bomberState

        ; THE GAME IS OVER, TERMINATE FUNC
;------------------------------------------


;---------------------------------------------- Middle
  middleExplosionEffect:
    JSR setMatIndexToBomb
     MiddleExpMobDeathVer:
        JSR CoordinateIsMob
        BNE bomberDeathMiddleExp
        ;JSR RenderMobDeath
        LDA #0
        STA mobIsAlive

    bomberDeathMiddleExp:
        JSR CoordinateIsBomber
        BNE endOfBombExplosionLogic
        LDA #0
        STA bomberState

        ; THE GAME IS OVER, TERMINATE FUNC

  endOfBombExplosionLogic:
   JSR ExplosionRender
   PLA
   TAX
   PLA
   TAY
   PLA
   RTS

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; MOB STUFF
MoveMobLogic:
    ;-------------------------------------------------------------------------------
    ; Push all registers (A, Y and X) to stack
    ;-------------------------------------------------------------------------------
    PHA
    TYA
    PHA
    TXA
    PHA

    LDA mobDirection

    LeftMobDirection:
        LDY #RIGHT_DIRECTION

        LDA mobDirection
        CMP #LEFT_DIRECTION
        BNE RightMobDirection

        ; Sets the new Mob Coordinates (X and Y)
        LDA mobX
        STA characterNewX
        LDA mobY
        STA characterNewY

        DEC characterNewX

        JSR ValidNewCoordinates
        BNE UpdateMobDirection

        JMP UpdateMobCoordinates

    RightMobDirection:
        LDY #UP_DIRECTION

        LDA mobDirection
        CMP #RIGHT_DIRECTION
        BNE UpMobDirection

        ; Sets the new Mob Coordinates (X and Y)
        LDA mobX
        STA characterNewX
        LDA mobY
        STA characterNewY

        INC characterNewX

        JSR ValidNewCoordinates
        BNE UpdateMobDirection

        JMP UpdateMobCoordinates

    UpMobDirection:
        LDY #DOWN_DIRECTION

        LDA mobDirection
        CMP #UP_DIRECTION
        BNE DownMobDirection

        ; Sets the new Mob Coordinates (X and Y)
        LDA mobX
        STA characterNewX
        LDA mobY
        STA characterNewY

        DEC characterNewY

        JSR ValidNewCoordinates
        BNE UpdateMobDirection

        JMP UpdateMobCoordinates

    DownMobDirection:
        LDY #LEFT_DIRECTION

        ; Sets the new Mob Coordinates (X and Y)
        LDA mobX
        STA characterNewX
        LDA mobY
        STA characterNewY

        INC characterNewY

        JSR ValidNewCoordinates
        BNE UpdateMobDirection

        JMP UpdateMobCoordinates

    UpdateMobCoordinates:
        LDA characterNewX
        STA mobX         ; Updates the X bomber variable with the new valid bomber position
        LDA characterNewY
        STA mobY         ; Updates the Y bomber variable with the new valid bomber position

        ; Updates the mob sprites. This subroutine is placed in graphics/engine.asm
        JSR MoveMobSprites

        ; Verifies if the new mob position coincides with the Bomber position
        JSR IsBomberKilledByMob
        BNE MoveMobLogicEnd     ; If not, just terminates the mob movement without doing anything
        ; Otherwise, the bomber is killed by the mob and the reset
        ; subroutine is called to reinitiallize the game
        LDA #0
        STA bomberState


        JMP MoveMobLogicEnd

    UpdateMobDirection:
        STY mobDirection

    MoveMobLogicEnd:
        ;-------------------------------------------------------------------------------
        ; Pull all registers (A, Y and X) from stack
        ;-------------------------------------------------------------------------------
        PLA
        TAX
        PLA
        TAY
        PLA

        RTS ; End of MoveBomberLogic subroutine
