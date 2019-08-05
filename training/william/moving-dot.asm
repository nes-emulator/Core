; ## Moving dot Game

; define points of use
define dotL          $00 ; dot location low byte
define dotH          $01 ; dot location high byte
define dotDirectionY $02 ; direction (possible values are below)
define dotDirectionX $03 ; direction (possible values are below)
define dotStart      $12 ; start of snake body byte pairs
define sXDirection   $14 ; control should move horizontally

; Directions (each using a separate bit)
define movingRight   1
define movingLeft    2

define movingUp      1
define movingDown    2

; System variables
define sysRandom    $fe

jsr init
jsr loop

init:
    jsr initDot
    jsr generateDotPosition
    rts

initDot:
    lda #movingRight 
    sta dotDirectionX

    lda #movingUp
    sta dotDirectionY
    rts

generateDotPosition:
    ;load a new random byte into $00
    lda sysRandom
    sta dotL

    ;load a new random number from 2 to 5 into $01
    lda sysRandom
    and #$03 ;mask out lowest 2 bits
    clc
    adc #2
    sta dotH

    rts

loop:
    jsr drawBlack
    jsr moveDotVertical
    jsr moveDotHorizontal
    jsr drawDot
    jsr spin
    jmp loop

moveDotHorizontal:
    lda dotDirectionX
    lsr 
    bcs right
    lsr
    bcs left
    rts

moveDotVertical:
    lda dotDirectionY
    lsr
    bcs up
    lsr 
    bcs down

up:
    lda dotL
    sec
    sbc #$20
    sta dotL
    bcc upup
    rts
upup:
    dec dotH
    lda #$1
    cmp dotH
    beq toggleDown
    rts

down:
    lda dotL
    clc
    adc #$20
    sta dotL
    bcs downdown
    rts
downdown:
    inc dotH
    lda #$6
    cmp dotH
    beq toggleUp
    rts

left:
    dec dotL
    dec dotL
    lda dotL
    and #$1f
    cmp #$1f
    beq toggleRight
    inc dotL
    rts

right:
    inc dotL
    inc dotL
    lda #$1f
    bit dotL
    beq toggleLeft
    dec dotL
    rts

toggleDown:
    lda dotL ; undo the extra up movement
    clc
    adc #$20
    sta dotL
    inc dotH
    lda #movingDown
    sta dotDirectionY
    lda #01
    sta sXDirection
    rts

toggleUp:
    lda dotL ; undo the extra down movement
    sec
    sbc #$20
    adc #$00
    sta dotL
    dec dotH
    lda #movingUp
    sta dotDirectionY
    lda #01
    sta sXDirection
    rts

toggleRight:
    inc dotL ; undo the extra left movement
    lda #movingRight
    sta dotDirectionX
    rts

toggleLeft:
    dec dotL ; undo the extra right movement
    lda #movingLeft
    sta dotDirectionX
    rts

drawBlack:
    ldx #0
    lda #0
    sta (dotL,x)
    rts

drawDot:
    ldx #0
    lda #1
    sta (dotL,x)
    rts

spin:
  ldx #0
spinloop:
  nop
  nop
  dex
  bne spinloop
  rts

gameOver:
