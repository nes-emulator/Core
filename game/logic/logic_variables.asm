;Variables to pass Index as parameter
    ;----------------------------
        matrixXIndex .dsb 1 ;
        matrixYIndex .dsb 1 ;
    ;----------------------------


    ;Variables to pass Index as parameter
    ;----------------------------
    characterNewX .dsb 1 ;
    characterNewY .dsb 1 ;
    ;----------------------------


    ;current bomber coordinates in logic matrix
    ;----------------------------------
    bomberX .dsb 1, #$01;alter -> start pos

    bomberY .dsb 1, #$01;alter -> start pos
    bomberState  .dsb 1, #ALIVE ; Game state
    bomberMovDirection .dsb 1 ;left,right,down or up: according the constants defined in this file

    BomberMoveCounter  .dsb 1,  #$00

    BomberDeathDelay .dsb 1

    buttons     .dsb 1


    ;----------------------------------

    DelayCounter .dsb 1, #0

    ;----------------------------------
    ;current mob coordinates in logic matrix
    mobX .dsb 1, #$00 ; alter

    mobY .dsb 1, #$00 ; alter

    mobDirection .dsb 1, #$01 ; left, right, down or up

    mobIsAlive .dsb 1, #ALIVE

    mobMoveCounter .dsb 1, #$00

    ;----------------------------------

    ;bomb manipulation

    ;BOMB EXPLOSION RANGE IS FIXED IN ONE RANGE CROSS
    ;----------------------------------
    bombX .dsb 1
    bombY .dsb 1

    bombCounter  .dsb 1
    bombIsActive .dsb 1, BOMB_DISABLED

    ;Explosion Boundaries, these variables are only used as parameters for the explosion render in graphics/* code
    expRightCoor .dsb 1 ; Possible values #AFFECTED or #NOT_AFFECTED
    expLeftCoor  .dsb 1
    expUpCoor    .dsb 1
    expDownCoor  .dsb 1

    numberOfBricksExploding .dsb 1 ;after ethe explosion of all bricks is finished this variable should store $#0 (NMI code)
    explodingBricksXCoor .dsb #BRICK_EXP_LIMIT
    explodingBricksYCoor .dsb #BRICK_EXP_LIMIT


    ;-----------------------------------------------
