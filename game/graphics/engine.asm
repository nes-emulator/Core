

   ; Graphics engine variable
   .enum $0700
   x_position       .dsb 1
   y_position       .dsb 1      ; Entry for methods
   initial_sprite   .dsb 1      ; Used for iteration on sprites

   sprites_size     .dsb 1      ; Count of how many active sprites

   ExplosionIsActive .dsb 1
   tickCounter .dsb 1
   expCounter .dsb 1
   MobIsAlive .dsb 1
   .ende

   BOMB_BASE_TIMER = $00
   MOB_MOV_INTERVAL = $00

;----------------
; Receives bomberman position as logical x_position and y_postion
; Moves all his sprites to screen position
;----------------
MoveBomberman:
    PHA
    TYA
    PHA
    TXA
    PHA                 ; Push all registers to stack

    LDA bomberX         ; Get logic X position
    ASL A
    ASL A
    ASL A
    ASL A               ; Multiply x position by 16

    STA x_position      ; Add x constant left space to complement (0)

    LDA bomberY         ; Get logic Y
    ASL A
    ASL A
    ASL A
    ASL A               ; Multiply y position by 16

    CLC
    ADC #$1F            ; Add y constant top space to complement (16)
    STA y_position      ; Save new value in same variable

ManageMoveBomberSprites:
    LDX #$00            ; Load sprite start position

    LDA y_position      ; Write first y position
    STA FIRST_SPRITE_Y, x

    JSR MoveXRegisterNextSprite
    LDA x_position      ; Write first x position
    STA FIRST_SPRITE_Y, x

    INX                 ; Go to next sprite of bomberman
    LDA y_position      ; Write second y position
    STA FIRST_SPRITE_Y, x

    JSR MoveXRegisterNextSprite
    LDA x_position
    CLC
    ADC #$08            ; Write second x, 8 bits ahead
    STA FIRST_SPRITE_Y, x

    INX                 ; Go to next sprite of bomberman
    LDA y_position
    CLC
    ADC #$08            ; Write third y, 8 bits ahead
    STA FIRST_SPRITE_Y, x

    JSR MoveXRegisterNextSprite
    LDA x_position      ; Write third x
    STA FIRST_SPRITE_Y, x

    INX                 ; Go to next sprite of bomberman
    LDA y_position
    CLC
    ADC #$08            ; Write fourth y, 8 bits ahead
    STA FIRST_SPRITE_Y, x

    JSR MoveXRegisterNextSprite
    LDA x_position
    CLC
    ADC #$08            ; Write fourth x, 8 bits ahead
    STA FIRST_SPRITE_Y, x

    PLA
    TAX
    PLA
    TAY
    PLA                 ; Pull all registers from stack

    RTS

MoveXRegisterNextSprite:
    INX                 ; Moves x to last part of sprite
    INX
    INX
    RTS


;----------------
; Receives bomberman direction as Register X
; Rotate his sprites to better fit screen
;----------------
MoveBombermanDirection:
    PHA
    TYA
    PHA
    TXA
    PHA                 ; Push registers

    LDA bomberMovDirection
    CMP #UP_MOVEMENT    ; Logic for decide which sprite to go for
    BEQ BombermanFacingUp

    CMP #DOWN_MOVEMENT
    BEQ BombermanFacingDown

    CMP #LEFT_MOVEMENT
    BEQ BombermanFacingLeft

    CMP #RIGHT_MOVEMENT
    BEQ BombermanFacingRight
    JMP MoveBombermanDirectionEnd

BombermanFacingRight:       ; Start of bomber facing left, horintally mirrored
    LDA #%01000000          ; Value to flip horizontally
    JSR MirrorSpritesHorizontally
    JSR ExchangeTilesRightOrder
    RTS                     ; Already returns on left/right flow
BombermanFacingLeft:
    LDA #$02                ; Start of bomber facing left sprite
    JSR MirrorSpritesHorizontally
    JSR ExchangeTilesLeftOrder
    RTS                     ; Return early on left/right flow

BombermanFacingUp:
    LDA #$0c                ; Start of bomber facing up sprite
    JMP MoveBombermanDirectionLoadSprite

BombermanFacingDown:
    LDA #$06                ; Start of bomber facing down sprite
    JMP MoveBombermanDirectionLoadSprite

MoveBombermanDirectionLoadSprite:
    STA initial_sprite      ; Next sprite
    JSR MirrorSpritesHorizontally

    LDX #$01                ; Write on first tile number
    STA FIRST_SPRITE_Y, x

    INC initial_sprite      ; Go to next sprite
    LDA initial_sprite

    JSR MoveXRegisterNextLine
    STA FIRST_SPRITE_Y, x   ; Write second tile number

    CLC
    ADC #$0F                ; Get down part of bomberman
    STA initial_sprite

    JSR MoveXRegisterNextLine
    STA FIRST_SPRITE_Y, x   ; Write third tile number

    INC initial_sprite      ; Go to next sprite
    LDA initial_sprite

    JSR MoveXRegisterNextLine
    STA FIRST_SPRITE_Y, x   ; Write fourth tile number

MoveBombermanDirectionEnd:
    PLA
    TAX
    PLA
    TAY
    PLA                     ; Return registers
    RTS

MoveXRegisterNextLine:
    INX                     ; Sum four
    INX
    INX
    INX
    RTS

; Receives Register A as entry for what to write on flip
MirrorSpritesHorizontally:
    LDX #$02
MirrorSpritesHorizontallyLoop:
    STA FIRST_SPRITE_Y, x  ; Write horizontal flip
    JSR MoveXRegisterNextLine
    CPX #$12               ; Until end of bomberman
    BNE MirrorSpritesHorizontallyLoop
    RTS

ExchangeTilesLeftOrder:
    LDX #$01               ; First left orientation tile
    LDA #$04               ; Reference to first sprite saved on A
    STA FIRST_SPRITE_Y, x

    JSR MoveXRegisterNextLine
    CLC
    ADC #$01               ; Second left tile
    STA FIRST_SPRITE_Y, x

    CLC
    ADC #$0F               ; Third left tile
    JSR MoveXRegisterNextLine
    STA FIRST_SPRITE_Y, x

    CLC
    ADC #$01               ; Last left tile
    JSR MoveXRegisterNextLine
    STA FIRST_SPRITE_Y, x

    RTS

ExchangeTilesRightOrder:
    LDX #$01               ; First right orientation tile
    LDA #$05               ; Reference to first sprite saved on A
    STA FIRST_SPRITE_Y, x

    JSR MoveXRegisterNextLine
    SEC
    SBC #$01               ; Second right tile
    STA FIRST_SPRITE_Y, x

    CLC
    ADC #$11               ; Third right tile
    JSR MoveXRegisterNextLine
    STA FIRST_SPRITE_Y, x

    SEC
    SBC #$01               ; Last right tile
    JSR MoveXRegisterNextLine
    STA FIRST_SPRITE_Y, x

    RTS

;----------------
; Move bomb control to next animation sprite
;----------------
BombNextAnimationStage:
    RTS

;----------------
; Reset all sprites past sprites_size
;----------------
ResetSprites:
    LDA #$FF
    LDX sprites_size
ResetSpritesLoop:
    STA FIRST_SPRITE_Y, x
    INX
    CPX #$00
    BNE ResetSpritesLoop

    RTS