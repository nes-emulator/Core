;;; CONSTANTS

MIDDLE_OPEN = %00000000
LEFT_WALL_OPEN = %01000000
LEFT_WALL_CLOSE = %01000100
RIGHT_WALL_OPEN = %00000100
RIGHT_WALL_CLOSE = %01000100

;; VARIABLE
matrix:
  .db %00000000, %00000000, %00000000, %00000000
  .db %00000000, %00000000, %00000000, %00000000    ; Space from top

  .db %01010101, %01010101, %01010101, %01010100    ; Top wall

  .db LEFT_WALL_OPEN, MIDDLE_OPEN, MIDDLE_OPEN, RIGHT_WALL_OPEN
  .db LEFT_WALL_CLOSE, LEFT_WALL_CLOSE, LEFT_WALL_CLOSE, RIGHT_WALL_CLOSE

  .db LEFT_WALL_OPEN, MIDDLE_OPEN, MIDDLE_OPEN, RIGHT_WALL_OPEN
  .db LEFT_WALL_CLOSE, LEFT_WALL_CLOSE, LEFT_WALL_CLOSE, RIGHT_WALL_CLOSE

  .db LEFT_WALL_OPEN, MIDDLE_OPEN, MIDDLE_OPEN, RIGHT_WALL_OPEN
  .db LEFT_WALL_CLOSE, LEFT_WALL_CLOSE, LEFT_WALL_CLOSE, RIGHT_WALL_CLOSE

  .db LEFT_WALL_OPEN, MIDDLE_OPEN, MIDDLE_OPEN, RIGHT_WALL_OPEN
  .db LEFT_WALL_CLOSE, LEFT_WALL_CLOSE, LEFT_WALL_CLOSE, RIGHT_WALL_CLOSE

  .db LEFT_WALL_OPEN, MIDDLE_OPEN, MIDDLE_OPEN, RIGHT_WALL_OPEN
  .db LEFT_WALL_CLOSE, LEFT_WALL_CLOSE, LEFT_WALL_CLOSE, RIGHT_WALL_CLOSE

  .db LEFT_WALL_OPEN, MIDDLE_OPEN, MIDDLE_OPEN, RIGHT_WALL_OPEN

  .db %01010101, %01010101, %01010101, %01010100     ; Bottom wall