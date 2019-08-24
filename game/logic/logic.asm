;-----------------------
;Constants
;------------------------
MAT_WALL = $00
MAT_PASS = $01
MAT_BRICK = $02
MT_ROWS = $0D ; 13
MT_COL =  $0F ; 15

;bomber movement constants
LEFT_MOVEMENT = $00
RIGHT_MOVEMENT = $01
DOWN_MOVEMENT = $10
UP_MOVEMENT = $11
ALIVE  = $01
DEAD = $00

;bomb constants
BOMB_ENABLED = $01
BOMB_DISABLED = $00

;----------------------------------
;Variables
;---------------------------------
 
 .enum $0200
    ;logic matrix to map logic to real positions
    ;15 * 13
    logicMatrix: 
        ;      0         1         2         3         4         5         6         7         8         9        10         11       12        13        14
        .db MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL ; 0 
        .db MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL ; 1
        .db MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL ; 2
        .db MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL ; 3
        .db MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL ; 4
        .db MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL ; 5
        .db MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL ; 6
        .db MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL ; 7
        .db MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL ; 8
        .db MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL ; 9
        .db MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL ; 10
        .db MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL ; 11
        .db MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL ; 12
        .db MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL, MAT_PASS, MAT_WALL ; 13
        .db MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL, MAT_WALL ; 14 

    
    
    ;Variables to pass Index as parameter
    ;---------------------------- 
        matrixXIndex .dsb 1 ;
        matrixYIndex .dsb 1 ;
    ;----------------------------

    



    ;current bomber coordinates in logic matrix 
    ;----------------------------------
    bomberX:
        .db $00;alter
    
    bomberY:
        .db $00;alter
    bomberState:
        .db ALIVE; Game state
    bomberMovDirection .dsb 1 ;left,right,down or up: according the constants defined in this file
    
    ;----------------------------------
    
    
    ;----------------------------------
    ;current mob coordinates in logic matrix
    MobX :
        .db $00 ; alter 
    MobY :
        .db $00 ; alter
    mobPositionIncrement :
        .db $01 ; 01 for + 1 and 0 for -1 (one direction)
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
pushRegisters:
    STA stkA
    PHA 
    TYA
    PHA
    TXA
    PHA
    LDA stkA
    RTS

pullRegisters:
    PLA
    TAX
    PLA
    TAY
    PLA
    RTS
;-------------------------------------------------------------------------------------
;matrix access subroutines

;Parameters: matrixYIndex
;Result -> change the A position to the begining of the line
;aux subroutine
positionAToIndexLine:
    LDA #$00
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
    JSR pushRegisters
    JSR coordinateIsBrick
    BEQ endOfIsWall
    JSR EndOfCoordinateIsBomb ; bombs are also walls
    BEQ endOfIsWall
    TAX
    LDA logicMatrix, x
    CMP #MAT_WALL
    endOfIsWall:
    JSR pullRegisters
    RTS


;Parameters: A = memory address positioned to X,Y coordinate
;if true, cmp flag  = 0
;aux subroutine
coordinateIsBrick:
    JSR pushRegisters
    TAX
    LDA logicMatrix, x
    CMP #MAT_BRICK
    JSR pullRegisters
    RTS

;Parameters: matrixXIndex and matrixYIndex
;if true, cmp flag  = 0
;aux subroutine
CordinateIsBomb:
    JSR pushRegisters
    LDA bombIsActive ; if bomb is not active, return
    CMP BOMB_ENABLED
    BNE EndOfCoordinateIsBomb ;not active
    LDA matrixXIndex
    CMP bombX
    BNE EndOfCoordinateIsBomb
    LDA matrixYIndex
    CMP bombY
    EndOfCoordinateIsBomb:
    JSR pullRegisters
    RTS

;Parameters: matrixXIndex and matrixYIndex
;if true, cmp flag  = 0
;aux subroutine    
CoordinateIsMob:
    JSR pushRegisters
    LDA matrixXIndex
    CMP MobX
    BNE EndOfCoordinateIsMob
    LDA matrixYIndex
    CMP MobY
    EndOfCoordinateIsMob:
    JSR pullRegisters
    RTS    
;----------------------------------------------------------------------------------------------------------------
;bomber MovementLogic



;Parameters -> movementDirection (left,right,up,down) (00,01,10,11 = constants defined in this file),
;movement directions is written in .NMI controller event
;this function will be called in the .NMI controller event
MoveBomber_Logic:
    JSR pushRegisters
    ;-----------------------------------------------------------------------------------------
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
    JSR pullRegisters
    RTS



