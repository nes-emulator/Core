;-----------------------
;Constants
;------------------------
LEFT_MOB_DIR = $01
RIGHT_MOB_DIR = $00


MAT_WALL = #2
MAT_PASS = #1
MAT_BRICK = #3

NUMBER_ROWS = #13 ; 13 -> was renamed to NUMBER_ROWS in joe's branch
NUMBER_COLUMNS =  #15 ; 15 -> was reanamed to NUMBER_COLUMNS in joe's branch
BOMB_BASE_TIMER = #90
BRICK_EXP_LIMIT = #3 ; the maximum number of bricks exploding at the same time is 3

;bomber movement constants,
LEFT_DIRECTION = $00 ; constant replaced to _DIRECTION in joe's branch
RIGHT_DIRECTION = $01 ;
DOWN_DIRECTION = $10 ;
UP_DIRECTION = $11

ALIVE  = $01 ;
DEAD = $00

BOMBER_MOVE_DELAY = #10

;bomb constants
BOMB_ENABLED = $01
BOMB_DISABLED = $00
NOT_AFFECTED = #0
AFFECTED = #1


;Mob constants
MOB_MOV_DELAY = #10

;---------------------------------------------------------
; bit:       7     6     5     4     3     2     1     0
; button:    A     B   select start  up   down  left right
A_BUTTON = %10000000
UP_BUTTON = %00001000
LEFT_BUTTON = %00000010
DOWN_BUTTON = %00000100
RIGHT_BUTTON = %00000001
