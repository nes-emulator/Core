;-----------------------
;Constants
;------------------------
MAT_WALL = $00
MAT_PASS = $01
MAT_BRICK = $02
MT_ROWS = $0D ; 13
MT_COL =  $0F ; 15
BOMB_BASE_TIMER = #120
BRICK_EXP_LIMIT = #3 ; the maximum number of bricks exploding at the same time is 3

;bomber movement constants
LEFT_MOVEMENT = $00
RIGHT_MOVEMENT = $01
DOWN_MOVEMENT = $10
UP_MOVEMENT = $11
ALIVE  = $01
DEAD = $00
PLAYER_MOV_DELAY = #30

;bomb constants
BOMB_ENABLED = $01
BOMB_DISABLED = $00
NOT_AFFECTED = #0
AFFECTED = #1

;Mob constants
MOB_MOV_INTERVAL = #60

;----------------------------------
;Variables
;---------------------------------
 
 .enum $0200
    ;logic matrix to map logic to real positions
    ;15 * 13
    logicMatrix: 
        ;      0         1         2         3         4         5         6         7         8         9        10         11       12        13        14
        .db MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL ; 0 
        .db MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS ; 1
        .db MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL ; 2
        .db MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS ; 3
        .db MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL ; 4
        .db MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS ; 5
        .db MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL ; 6
        .db MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS ; 7
        .db MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL ; 8
        .db MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS ; 9
        .db MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL ; 10
        .db MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS, MAT_PASS ; 11
        .db MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL ; 12       
        
        
        
            
    
    ;Variables to pass Index as parameter
    ;---------------------------- 
        matrixXIndex .dsb 1 ;
        matrixYIndex .dsb 1 ;
    ;----------------------------

    



    ;current bomber coordinates in logic matrix 
    ;----------------------------------
    bomberX:
        .db $01;alter -> start pos
    
    bomberY:
        .db $01;alter -> start pos
    bomberState:
        .db ALIVE;  Game state
    bomberMovDirection .dsb 1 ;left,right,down or up: according the constants defined in this file

    BomberMoveCounter:
        .db $0;  
    ;----------------------------------
    
    
    ;----------------------------------
    ;current mob coordinates in logic matrix
    MobX :
        .db $00 ; alter 
    MobY :
        .db $00 ; alter
    mobPositionIncrement :
        .db $01 ; 01 for + 1 and 0 for -1 (one direction)
    mobIsAlive:
        .db #ALIVE
    mobMoveCounter:
        .db #0
    ;----------------------------------
    
    ;bomb manipulation

    ;BOMB EXPLOSION RANGE IS FIXED IN ONE RANGE CROSS
    ;----------------------------------
    bombIsActive:
        .db BOMB_DISABLED
    bombCounter  .dsb 1

    bombX .dsb 1
    bombY .dsb 1

    ;Explosion Boundaries, these variables are only used as parameters for the explosion render in graphics/* code
    expRightCoor .dsb 1 ; Possible values #AFFECTED or #NOT_AFFECTED
    expLeftCoor  .dsb 1
    expUpCoor    .dsb 1
    expDownCoor  .dsb 1

    
    numberOfBricksExploding .dsb 1 ;after ethe explosion of all bricks is finished this variable should store $#0 (NMI code)
    explodingBricksXCoor .dsb #BRICK_EXP_LIMIT 
    explodingBricksYCoor .dsb #BRICK_EXP_LIMIT
    

    ;-----------------------------------------------
       

.ende


;-----------------------------------------------------------------
;stack functions

;TODO: Move stack functions to game.asm
;you need to call these function before every function
;in which you dont want to preserve the state of the 3 registers

;-------------------------------------------------------------------------------------
;matrix access subroutines

;Parameters: matrixYIndex
;Result -> change the A position to matrix offset, NOT THE BEGINING OF THE ADDRESS
;aux subroutine
positionAToIndexLine:
    LDA #$0
    LDY matrixYIndex
    linePositioningLoop:
        CPY $0
        BEQ linePositioningLoopEnd
        DEY 
        CLC
        ADC #MT_COL
        JMP linePositioningLoop
    linePositioningLoopEnd:
    RTS 
 


;Parameters: matrixXIndex and matrixYIndex
;change A to matrixXIndex, matrixYIndex position
;aux subroutine
accessLogicMatrixCoordinate:
    JSR positionAToIndexLine ;sum NLINES*y to index coordinate
    CLC
    ADC matrixXIndex ;sum x to index
    ;Now A is in the specific cell
    RTS
;-----------------------------------------------------------------------------------------------------------------
;matrix verification subroutines

;Parameters: A = memory address positioned to X,Y coordinate and ; matrixXIndex and matrixYIndex
;if true, cmp flag  = 0
;aux subroutine
coordinateIsWall:
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
    JSR EndOfCoordinateIsBomb ; bombs are also walls
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
coordinateIsBrick:
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

;Parameters: matrixXIndex and matrixYIndex
;if true, cmp flag  = 0
;aux subroutine
CordinateIsBomb:
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
    LDA matrixXIndex
    CMP bombX
    BNE EndOfCoordinateIsBomb
    LDA matrixYIndex
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

;Parameters: matrixXIndex and matrixYIndex
;if true, cmp flag  = 0
;aux subroutine    
CoordinateIsMob:
    ;--------------------------------------- push all
    STA stkA
    PHA 
    TYA
    PHA
    TXA
    PHA
    LDA stkA
    ;---------------------------------------
    LDA matrixXIndex
    CMP MobX
    BNE EndOfCoordinateIsMob
    LDA matrixYIndex
    CMP MobY
    EndOfCoordinateIsMob:
    ;---------------- Pull All
    PLA
    TAX
    PLA
    TAY
    PLA
    ;-------------------------
    RTS

;Parameters: matrixXIndex and matrixYIndex
;if true, cmp flag  = 0
;aux subroutine    
CoordinateIsBomber:
    ;--------------------------------------- push all
    STA stkA
    PHA 
    TYA
    PHA
    TXA
    PHA
    LDA stkA
    ;---------------------------------------
    LDA matrixXIndex
    CMP bomberX
    BNE EndOfCoordinateIsBomber
    LDA matrixYIndex
    CMP bomberY
    EndOfCoordinateIsBomber:
    ;---------------- Pull All
    PLA
    TAX
    PLA
    TAY
    PLA
    ;-------------------------
    RTS      
;----------------------------------------------------------------------------------------------------------------
;bomber MovementLogic




;Parameters -> movementDirection (left,right,up,down) (00,01,10,11 = constants defined in this file),
;movement directions is written in .NMI controller event
;this function will be called in the .NMI controller event
MoveBomber_Logic:
    ;--------------------------------------- push all
    STA stkA
    PHA 
    TYA
    PHA
    TXA
    PHA
    LDA stkA
    ;---------------------------------------
    ;-----------------------------------------------------------------------------------------
    LDA bomberX
    STA matrixXIndex
    LDA bomberY
    STA matrixYIndex

    LDA bomberMovDirection
       
    ;First: choose rotate direction
    ;this code will update the coordinate of the indexed cell acordingly to bomber movement direction 
    ;and call the rotate 'PPU' code.
    
    CMP #LEFT_MOVEMENT
    BNE rightMov
        LDX matrixXIndex
        DEX 
        STX matrixXIndex
        ;JRS rotateBomberLeft (EDINHA)
    JMP endOfMovementDirVerification
    
    rightMov:
        CMP #RIGHT_MOVEMENT
        BNE downMov
            LDX matrixXIndex
            INX 
            STX matrixXIndex
            ;JRS rotateBomberRight (EDINHA)
        JMP endOfMovementDirVerification

    downMov:
        CMP #DOWN_MOVEMENT
        BNE upMov
            LDX matrixYIndex
            INX 
            STX matrixYIndex
            ;JRS rotateBomberDown (EDINHA)
        JMP endOfMovementDirVerification

    upMov:
        LDX matrixYIndex
        DEX 
        STX matrixYIndex
        ;JRS rotateBomberUp (EDINHA)

    endOfMovementDirVerification:
    ;-----------------------------------------------------------------------------------------
    JSR accessLogicMatrixCoordinate  ; shift 'A' to cell position of matrixXIndex , matrixXIndex       

    LDX mobIsAlive
    CMP #ALIVE
    BNE wallVerificationBomberMov ;if mob isn't alive, there is no need to verify
    JSR CoordinateIsMob ; A is a parameter
    BEQ KilledInMovByMob

    wallVerificationBomberMov:
    JSR coordinateIsWall ; wall also cover bomb case, A and matrixXindex and matrixYIndex are parameters
    BEQ EndOfBomberMov

    ;update bomber coordinates after validation
    LDA matrixXIndex
    STA bomberX
    LDA matrixYIndex
    STA bomberY
    ;JSR movBomber_graphic (Edinha)
    

    KilledInMovByMob:
        LDA DEAD
        STA bomberState
        ;JSR DeathAnimation (EDINHA)        

    EndOfBomberMov:
    ;---------------- Pull All
    PLA
    TAX
    PLA
    TAY
    PLA
    ;-------------------------
    RTS


;tickCounter = 0
;bombIsActive = 1 
;bombCounter = 0
;update bomb coordinate
;place the bomb in the current bomber coordinate position
placeBomb:
    ;--------------------------------------- push all
    STA stkA
    PHA 
    TYA
    PHA
    TXA
    PHA
    LDA stkA
    ;---------------------------------------
    
    LDA bombIsActive
    CMP #Enabled
    BEQ endOfPlaceBomb ;if an active bomb already exists, terminate 

    ;change bomb coordinate to bomberman coordinate
    LDA bomberX
    STA bombX
    LDA bomberY
    STA bombY

    ;JSR renderBomb (EDINHA), look at bomb coordinates (bombX,bombY)

    ;update flags
    LDA #BOMB_ENABLED
    STA bombIsActive
    LDA #$0
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

;TODO: a refactor (function extraction) would be nice, in order to save space
;Flags to set:
;ExplosionIsActive  = 1
;expCounter = 0
;bombIsActive = 0
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
  LDA #$01
  STA ExplosionIsActive ;activate explosion
  
  ;all sides of the explosion animation start Enabled, the explosion is only limited by walls
  LDA #AFFECTED
  STA expLeftCoor
  STA expRightCoor
  STA expUpCoor
  STA expDownCoor
  
  ;Verify all four adjacent squares individualy   
  LDA bombX
  STA matrixXIndex
  LDA bombY
  STA matrixYIndex
  
  ;RIGHT
;---------------------------------------  
  LDX matrixXIndex
  INX
  STX matrixXIndex
  JSR accessLogicMatrixCoordinate ;change A to 
  JSR coordinateIsWall
  BNE rightExpMobDeathVer ;if the coordinate affected is not a wall
  LDX #NOT_AFFECTED ;the right side wasn't affected by the explosion
  STX expRightCoor
  ;---------------------------------------------------------
  rightBrickExpVer:
  JSR coordinateIsBrick
  BNE rightExpMobDeathVer
  TAX ; X = cell offset
  LDA #MAT_PASS
  STA logicMatrix, x ; the position is no longer a logic wall, EDINHA's exploding brick animation will be called in NMI,
  ;by inspecting numberOfBricksExploding
  LDX numberOfBricksExploding
  LDA matrixXIndex
  STA explodingBricksXCoor, x 
  LDA matrixYIndex
  STA explodingBricksYCoor, x
  INX 
  STX numberOfBricksExploding
 ;------------------------------------------------------------
  rightExpMobDeathVer:
    JSR CoordinateIsMob
    BNE bomberDeathRightExp
    LDA #DEAD
    STA mobIsAlive
    ; JSR MOB DEATH ANIMATION (EDINHA)
 
  bomberDeathRightExp:
    JSR CoordinateIsBomber
    BNE checkLeftExplosionEffect
    LDA #DEAD
    STA bomberState
    ;JSR BOMBER DEATH ANIMATION (EDINHA)
    JMP endOfBombExplosion ; THE GAME IS OVER, TERMINATE FUNC
 ;---------------------------------------------
 
 ;restore parameter coordinates
  LDA bombX
  STA matrixXIndex
 
 ;LEFT
 ;----------------------------------------------------------------
  checkLeftExplosionEffect:

  LDX matrixXIndex
  DEX
  STX matrixXIndex
  JSR accessLogicMatrixCoordinate ;change A to matrixOffset
  JSR coordinateIsWall
  BNE leftExpMobDeathVer ;if the coordinate affected is not a wall
  LDX #NOT_AFFECTED ;the right side wasn't affected by the explosion
  STX expLeftCoor
  ;---------------------------------------------------------
  leftBrickExpVer:
  JSR coordinateIsBrick
  BNE leftExpMobDeathVer
  TAX ; X = cell offset
  LDA #MAT_PASS
  STA logicMatrix, x ; the position is no longer a logic wall, EDINHA's exploding brick animation will be called in NMI,
  ;by inspecting numberOfBricksExploding
  LDX numberOfBricksExploding
  LDA matrixXIndex
  STA explodingBricksXCoor, x 
  LDA matrixYIndex
  STA explodingBricksYCoor, x
  INX 
  STX numberOfBricksExploding
 ;------------------------------------------------------------
  leftExpMobDeathVer:
    JSR CoordinateIsMob
    BNE bomberDeathLeftExp
    LDA #DEAD
    STA mobIsAlive
    ; JSR MOB DEATH ANIMATION (EDINHA)
 
  bomberDeathLeftExp:
    JSR CoordinateIsBomber
    BNE checkUpExplosionEffect
    LDA #DEAD
    STA bomberState
    ;JSR BOMBER DEATH ANIMATION (EDINHA)
    JMP endOfBombExplosion ; THE GAME IS OVER, TERMINATE FUNC
 ;----------------------------------------------------------------

;restore parameter coordinates
  LDA bombX
  STA matrixXIndex
 
 ;UP
 ;-------------------------------------------
  checkUpExplosionEffect:
    LDX matrixYIndex
    DEX
    STX matrixYIndex
    JSR accessLogicMatrixCoordinate ;change A to 
    JSR coordinateIsWall
    BNE UpExpMobDeathVer ;if the coordinate affected is not a wall
    LDX #NOT_AFFECTED ;the right side wasn't affected by the explosion
    STX expUpCoor
    ;---------------------------------------------------------
    UpBrickExpVer:
    JSR coordinateIsBrick
    BNE UpExpMobDeathVer
    TAX ; X = cell offset
    LDA #MAT_PASS
    STA logicMatrix, x ; the position is no longer a logic wall, EDINHA's exploding brick animation will be called in NMI,
    ;by inspecting numberOfBricksExploding
    LDX numberOfBricksExploding
    LDA matrixXIndex
    STA explodingBricksXCoor, x 
    LDA matrixYIndex
    STA explodingBricksYCoor, x
    INX 
    STX numberOfBricksExploding
    ;------------------------------------------------------------
    UpExpMobDeathVer:
        JSR CoordinateIsMob
        BNE bomberDeathUpExp
        LDA #DEAD
        STA mobIsAlive
        ; JSR MOB DEATH ANIMATION (EDINHA)
    
    bomberDeathUpExp:
        JSR CoordinateIsBomber
        BNE checkDownExplosionEffect
        LDA #DEAD
        STA bomberState
        ;JSR BOMBER DEATH ANIMATION (EDINHA)
        JMP endOfBombExplosion ; THE GAME IS OVER, TERMINATE FUNC
 ;--------------------------------------------

;restore parameter coordinates
  LDA bombY
  STA matrixYIndex
 
 ;DOWN
 ;------------------------------------------
    checkDownExplosionEffect:
    LDX matrixYIndex
    INX
    STX matrixYIndex
    JSR accessLogicMatrixCoordinate ;change A to 
    JSR coordinateIsWall
    BNE DownExpMobDeathVer ;if the coordinate affected is not a wall
    LDX #NOT_AFFECTED ;the right side wasn't affected by the explosion
    STX expDownCoor
    ;---------------------------------------------------------
    DownBrickExpVer:
    JSR coordinateIsBrick
    BNE DownExpMobDeathVer
    TAX ; X = cell offset
    LDA #MAT_PASS
    STA logicMatrix, x ; the position is no longer a logic wall, EDINHA's exploding brick animation will be called in NMI,
    ;by inspecting numberOfBricksExploding
    LDX numberOfBricksExploding
    LDA matrixXIndex
    STA explodingBricksXCoor, x 
    LDA matrixYIndex
    STA explodingBricksYCoor, x
    INX 
    STX numberOfBricksExploding
    ;------------------------------------------------------------
    DownExpMobDeathVer:
        JSR CoordinateIsMob
        BNE bomberDeathDownExp
        LDA #DEAD
        STA mobIsAlive
        ; JSR MOB DEATH ANIMATION (EDINHA)
    
    bomberDeathDownExp:
        JSR CoordinateIsBomber
        BNE endOfBombExplosion
        LDA #DEAD
        STA bomberState
        ;JSR BOMBER DEATH ANIMATION (EDINHA)
        ; THE GAME IS OVER, TERMINATE FUNC
;------------------------------------------

  ;JSR ExplosionAnimation (EDINHA) -> this call can be placed here or in NMI using ticks and expCounter
  
  endOfBombExplosion:
  ;---------------- Pull All
    PLA
    TAX
    PLA
    TAY
    PLA
  ;-------------------------
    
    RTS
