;-----------------------
;Constants
;------------------------
MAT_WALL = $00
MAT_PASS = $01
MAT_BRICK = $02
MT_ROWS = $0D ; 13
MT_COL =  $0F ; 15
BOMB_BASE_TIMER = #120


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
    ;----------------------------------
    bombIsActive:
        .db BOMB_DISABLED
    bombCounter  .dsb 1

    bombX .dsb 1
    bombY .dsb 1
       

.ende


;-----------------------------------------------------------------
;stack functions

;TODO: Move stack functions to game.asm
;you need to call these function before every function
;in which you dont want to preserve the state of the 3 registers

;-------------------------------------------------------------------------------------
;matrix access subroutines

;Parameters: matrixYIndex
;Result -> change the A position to the begining of the line
;aux subroutine
positionAToIndexLine:
    LDA logicMatrix
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

    JSR CoordinateIsMob ; A is a parameter
    BEQ KilledInMovByMob

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
    
    ;---------------- Pull All
    PLA
    TAX
    PLA
    TAY
    PLA
    ;-------------------------
    RTS


;ExplosionIsActive  = 1
;expCounter = 0
;bombIsActive = 0
;center pos -> return
;when the bomb explodes
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




  ;---------------- Pull All
    PLA
    TAX
    PLA
    TAY
    PLA
  ;-------------------------

