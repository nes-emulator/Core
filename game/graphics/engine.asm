; CONSTANTS

   MOB_SPRITE_START_POSITION = $10
   BOMB_SPRITE_START_POSITION = $20
   EXPLOSION_SPRITE_START_POSITION = $30

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
    STA x_position
    LDA bomberY         ; Get logic Y position
    STA y_position

    JSR CalculateScreenPosition

ManageMoveBomberSprites:
    LDX #$00            ; Load sprite start position

    LDA y_position      ; Write first y position
    STA FIRST_SPRITE_Y, x

    LDA x_position      ; Write first x position
    STA FIRST_SPRITE_X, x

    JSR MoveXRegisterNextLine

    LDA y_position      ; Write second y position
    STA FIRST_SPRITE_Y, x

    LDA x_position_fix
    STA FIRST_SPRITE_X, x

    JSR MoveXRegisterNextLine

    LDA y_position_fix
    STA FIRST_SPRITE_Y, x

    LDA x_position      ; Write third x
    STA FIRST_SPRITE_X, x

    JSR MoveXRegisterNextLine

    LDA y_position_fix  ; Write fourth line
    STA FIRST_SPRITE_Y, x

    LDA x_position_fix
    STA FIRST_SPRITE_X, x

    PLA
    TAX
    PLA
    TAY
    PLA                 ; Pull all registers from stack

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
    CMP #UP_DIRECTION    ; Logic for decide which sprite to go for
    BEQ BombermanFacingUp

    CMP #DOWN_DIRECTION
    BEQ BombermanFacingDown

    CMP #LEFT_DIRECTION
    BEQ BombermanFacingLeft

    CMP #RIGHT_DIRECTION
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


; Calculate x and y anchor fix positions
CalculateScreenPosition:
    LDA #00
MultiplyBy16Loop:
    ASL x_position        ; Multiply both entries by 2
    ASL y_position
    CLC
    ADC #01
    CMP #$04              ; Do it four time, goes to x16 of entries
    BNE MultiplyBy16Loop

    LDA x_position
    CLC                   ; Calculate bottom anchor position x
    ADC #$08
    STA x_position_fix

    LDA y_position
    CLC
    ADC #$1F            ; Add y constant top space to complement (16)

    STA y_position      ; Save new value in same variable
    CLC                 ; Calculate bottom anchor position y
    ADC #$08
    STA y_position_fix
    RTS

;----------------
; Move bomb control to next animation sprite
;----------------
BombNextAnimationStage:
    RTS

;----------------
; First render of bomb sprite
;----------------
BombRender:
    LDA bombX           ; Get logic X position
    STA x_position
    LDA bombY           ; Get logic Y position
    STA y_position

    LDA #$C8            ; Initial sprite of bomb
    STA initial_sprite

    LDX #BOMB_SPRITE_START_POSITION
    JSR RenderSpriteGroup

    RTS


;----------------
; First render of bomberman death animation
;----------------
RenderBombermanDeath:
    LDA bomberX         ; Get logic X position
    STA x_position
    LDA bomberY         ; Get logic Y position
    STA y_position

    LDA #$28            ; Initial death sprite
    STA initial_sprite

    LDX #$00            ; Bomberman sprite PPU position
    JSR RenderSpriteGroup

    RTS

;----------------
; First render of explosion sprite
;----------------
ExplosionRender:
    LDA bombX         ; Copying explosion center position
    STA x_position
    LDA bombY
    STA y_position

    LDA #$4C          ; Sprite center explosion
    STA initial_sprite

    LDX #BOMB_SPRITE_START_POSITION
    JSR RenderSpriteGroup

    LDA expRightCoor
    CMP #AFFECTED
    BNE ExplosionLeftRender

ExplosionRightRender:
    LDA bombX         ; Copying explosion center position
    STA x_position
    LDA bombY
    STA y_position

    INC x_position    ; Make explosion to right

    LDA #$4C          ; Sprite center explosion
    STA initial_sprite

    LDA #BOMB_SPRITE_START_POSITION
    CLC               ; Calculate next start position
    ADC #$10
    TAX
    JSR RenderSpriteGroup

ExplosionLeftRender:
    LDA expLeftCoor
    CMP #AFFECTED
    BNE ExplosionUpRender

    LDA bombX         ; Copying explosion center position
    STA x_position
    LDA bombY
    STA y_position

    DEC x_position    ; Make explosion to left

    LDA #$4C          ; Sprite center explosion
    STA initial_sprite

    LDA #BOMB_SPRITE_START_POSITION
    CLC               ; Calculate next start position
    ADC #$20
    TAX
    JSR RenderSpriteGroup


ExplosionUpRender:
    LDA expUpCoor
    CMP #AFFECTED
    BNE ExplosionDownRender

    LDA bombX         ; Copying explosion center position
    STA x_position
    LDA bombY
    STA y_position

    DEC y_position    ; Make explosion to up

    LDA #$4C          ; Sprite center explosion
    STA initial_sprite

    LDA #BOMB_SPRITE_START_POSITION
    CLC               ; Calculate next start position
    ADC #$30
    TAX
    JSR RenderSpriteGroup


ExplosionDownRender:
    LDA expDownCoor
    CMP #AFFECTED
    BNE ExplosionRenderEnd

    LDA bombX         ; Copying explosion center position
    STA x_position
    LDA bombY
    STA y_position

    INC y_position    ; Make explosion to down

    LDA #$4C          ; Sprite center explosion
    STA initial_sprite

    LDA #BOMB_SPRITE_START_POSITION
    CLC               ; Calculate next start position
    ADC #$40
    TAX
    JSR RenderSpriteGroup

ExplosionRenderEnd:
    RTS

;----------------
; Removes render of explosion sprites
;----------------
RemoveExplosionRender:
    LDA #BOMB_SPRITE_START_POSITION
    CLC
    ADC #$4F           ; Go to last explosion sprite
    TAX
    LDA #$FF           ; Reset bomb value
RemoveExplosionRenderLoop:
    STA FIRST_SPRITE_Y, x
    DEX                ; On loop apply reset
    CPX #BOMB_SPRITE_START_POSITION
    BNE RemoveExplosionRenderLoop

    RTS

;----------------
; Render the sprite group of 4 tiles on screen based on entry variables
;
; X register must be set as offset from PPU sprites position start
; x_position and y_position initial must be set beforehand
; control_sprite is the sprite control flags
; initial_sprite is the tile reference
;----------------
RenderSpriteGroup:
    JSR CalculateScreenPosition

    LDY y_position
    LDA x_position
    JSR RenderSprite    ; First line sprite draw
    JSR MoveXRegisterNextLine

    INC initial_sprite  ; Second line sprite draw
    LDA x_position_fix
    JSR RenderSprite
    JSR MoveXRegisterNextLine

    LDA initial_sprite
    CLC
    ADC #$0F            ; Move sprite reference tile to chr line below
    STA initial_sprite

    LDA x_position      ; Third line sprite draw
    LDY y_position_fix
    JSR RenderSprite
    JSR MoveXRegisterNextLine

    INC initial_sprite  ; Last line sprite draw
    LDA x_position_fix
    JSR RenderSprite

    RTS


;----------------
; Render the sprite on screen based on entry variables
;
; X register on the sprite PPU position ($0200 + x)
; A register is the sprite X position
; Y register is the sprite Y position
; control_sprite is the sprite control flags
; initial_sprite is the tile reference
;----------------
RenderSprite:
    STA FIRST_SPRITE_X, x
    TYA                 ; Render both X and Y position
    STA FIRST_SPRITE_Y, x

    LDA initial_sprite
    STA FIRST_SPRITE_TILE, x

    LDA #$00
    STA FIRST_SPRITE_CONTROL, x

    RTS

; ;;;;;;;;;;;;;;;;;;; MOB STUFF
; ;-------------------------------------------------------------------------------
; ;-------------------------------------------------------------------------------
; ; Receives mob position as logical x_position and y_postion
; ; Moves all his sprites to screen position
; ;-------------------------------------------------------------------------------
; ;-------------------------------------------------------------------------------
MoveMobSprites:
    ;-------------------------------------------------------------------------------
    ; Push all registers (A, Y and X) to stack
    ;-------------------------------------------------------------------------------
    PHA
    TYA
    PHA
    TXA
    PHA

    LDA mobX         ; Get logic X position
    STA x_position
    LDA mobY         ; Get logic Y position
    STA y_position

    JSR CalculateScreenPosition

    ManageMoveMobSprites:
        LDX #$00            ; Load sprite start position

        LDA y_position      ; Write first y position
        STA FIRST_MOB_Y, x

        LDA x_position      ; Write first x position
        STA FIRST_MOB_X, x

        JSR MoveXRegisterNextLine

        LDA y_position      ; Write second y position
        STA FIRST_MOB_Y, x

        LDA x_position_fix
        STA FIRST_MOB_X, x

        JSR MoveXRegisterNextLine

        LDA y_position_fix
        STA FIRST_MOB_Y, x

        LDA x_position      ; Write third x
        STA FIRST_MOB_X, x

        JSR MoveXRegisterNextLine

        LDA y_position_fix  ; Write fourth line
        STA FIRST_MOB_Y, x

        LDA x_position_fix
        STA FIRST_MOB_X, x

    ;-------------------------------------------------------------------------------
    ; Pull all registers (A, Y and X) from stack
    ;-------------------------------------------------------------------------------
    PLA
    TAX
    PLA
    TAY
    PLA
    RTS


;----------------
; First render of mob death animation
;----------------
RenderMobDeath:
    LDA mobX            ; Get logic X position
    STA x_position
    LDA mobY            ; Get logic Y position
    STA y_position

    LDA #$48            ; Initial death sprite
    STA initial_sprite

    LDX #$10            ; Mob sprite PPU position
    JSR RenderSpriteGroup

    RTS