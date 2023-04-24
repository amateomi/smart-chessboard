from enum import Enum


class State(Enum):
    START = 1
    USER_MOVE = 2
    AI_MOVE = 3
    SELECT_CAPTURE = 4
    MOVE_PROCESS = 5
    PAWN_PROMOTION = 6
    GAME_OVER_CHECK = 7
