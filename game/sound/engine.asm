; Constants
SQ1_ENV = $4000
SQ1_LO = $4002
SQ1_HI = $4003

TRI_CTRL = $4008
TRI_LO = $400A
TRI_HI = $400B

; Variable

explosionSFX .dsb 1 ;
bombSFX .dsb 1 ;

; Sound engine reserved RAM: 76C to 7FF
; .enum $#76C
;
; .ende

; Eternal Beep
EternalBeep:
    LDA #%10110010; Duty 10 (50%), volume 2
    STA SQ1_ENV
    lda #$C9    ;0C9 is a C# in NTSC mode
    sta SQ1_LO
    lda #$00
    sta SQ1_HI
    RTS

ClearSQ1:
    LDA #0
    STA SQ1_ENV
    STA SQ1_LO
    STA SQ1_HI
    RTS

TriangleOn:
    LDA #%10000001
    STA TRI_CTRL
    lda #$42   ;a period of $042 plays a G# in NTSC mode.
    sta $400A
    lda #$00
    sta $400B
    RTS

TriangleOff:
    LDA #%10000000
    STA TRI_CTRL
    RTS

soundEngine:
    RTS
