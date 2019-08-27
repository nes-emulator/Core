; Constants

    ; TEMPO
    TICK_TEMPO = #16
    EXPL_TEMPO = #4

    ; ADDRESSES
    APUFLAGS = $4015    ; setup the APU

    SQ1_ENV = $4000     ; SQUARE 1
    SQ1_LO = $4002
    SQ1_HI = $4003

    SQ2_ENV = $4004     ; SQUARE 2
    SQ2_LO = $4006
    SQ2_HI = $4007

    TRI_ENV = $4008     ; Triangle
    TRI_LO = $400A
    TRI_HI = $400B

    NOISE_ENV = $400C   ; Noise

; Variables

.enum $1800
   .include "sound/sound_variables.asm"
.ende

    ; A flag that is set when the engine should play a explosion SFX
    ; sound_flag_expl .dsb 1

    ; A flag that is set when the engine should play a tick SFX
    ; sound_flag_tick .dsb 1

    ; Counter to control the tempo of the notes
    ; sound_frame_counter .dsb 1


; Sets the bomb tick flag
sound_bomb_tick:
    PHA

    LDA #1
    STA sound_flag_tick

    PLA
    RTS

; Sets the bomb explosion flag
sound_bomb_expl:
    PHA

    LDA #1
    STA sound_flag_expl

    PLA
    RTS

; Call this in Reset to setup the APU
sound_init:
    LDA #%00001111
    STA APUFLAGS   ;enable Square 1, Square 2, Triangle and Noise channels

    LDA #$30
    STA SQ1_ENV     ;set Square 1 volume to 0
    STA SQ2_ENV     ;set Square 2 volume to 0
    STA NOISE_ENV   ;set Noise volume to 0
    LDA #$80
    STA TRI_ENV   ;silence Triangle

    ; Clear counters and flags
    LDA #0
    STA sound_frame_counter
    STA sound_flag_tick
    STA sound_flag_expl

    RTS

Beep:
    LDA #%10111111 ; Duty 10 (50%), volume 15
    STA SQ1_ENV
    LDA #$C9    ;0C9 is a C# in NTSC mode
    STA SQ1_LO
    LDA #$00
    STA SQ1_HI
    RTS

ClearSQ1:
    LDA #0
    STA SQ1_ENV
    STA SQ1_LO
    STA SQ1_HI
    RTS

TriangleOn:
    LDA #%10000001
    STA TRI_ENV
    lda #$42   ;a period of $042 plays a G# in NTSC mode.
    sta $400A
    lda #$00
    sta $400B
    RTS

TriangleOff:
    LDA #%10000000
    STA TRI_ENV
    RTS


;;; Noise seems to not play any sound.
; NoiseTest:
;     LDA #%00110111
;     STA $400C
;     LDA #%00000111
;     STA $400E
;     RTS
;
; NoiseOn:
;     LDA #%00110100
;     STA NOISE_ENV
;     RTS
;
; NoiseOff:
;     LDA #0
;     STA NOISE_ENV
;     RTS

sound_play_frame:

    ; tick:
    ;     LDA sound_flag_tick
    ;     CMP #1
    ;     BNE explosion
    ;         ; play the tick
    ;         JSR TriangleOn
    ;         INC sound_frame_counter
    ;         LDA sound_frame_counter
    ;         ; CMP #TICK_TEMPO
    ;         CMP #16
    ;         BNE explosion
    ;             ; end SFX
    ;             LDA #0
    ;             STA sound_flag_tick
    ;             STA sound_frame_counter
    ;             JSR TriangleOff

    explosion:
        LDA sound_flag_expl
        CMP #1
        BNE sound_done
            JSR Beep
            INC sound_frame_counter
            LDA sound_frame_counter
            CMP #EXPL_TEMPO
            BNE sound_done
                ; end SFX
                LDA #0
                STA sound_flag_expl
                STA sound_frame_counter
                JSR ClearSQ1

    sound_done:
        RTS
