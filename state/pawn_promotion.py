import chess

import hardware_interaction as hw
from constants import PAWN_PROMOTION_STRING_OPTIONS, PAWN_PROMOTION_OPTIONS
from state.state_machine import State

pawn_promotion_index = 0  # Used for indexing in PAWN_PROMOTION_STRING_OPTIONS and PAWN_PROMOTION_OPTIONS


def pawn_promotion(move: chess.Move) -> tuple[State, chess.Move | None]:
    global pawn_promotion_index
    print(f"Select piece {PAWN_PROMOTION_STRING_OPTIONS[pawn_promotion_index]}?")
    if hw.is_select_button_pressed():
        move.promotion = PAWN_PROMOTION_OPTIONS[pawn_promotion_index]
        pawn_promotion_index = 0
        return State.MOVE_PROCESS, move
    elif hw.is_left_button_pressed() and pawn_promotion_index > 0:
        pawn_promotion_index -= 1
    elif hw.is_right_button_pressed() and pawn_promotion_index < len(PAWN_PROMOTION_STRING_OPTIONS) - 1:
        pawn_promotion_index += 1
    return State.PAWN_PROMOTION, None
