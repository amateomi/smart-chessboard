import time

import chess

import hardware_interaction as hw
from state.state_machine import State


def game_over_check(board: chess.Board) -> State:
    if board.is_check():
        hw.print_to_display(["Check!"])
        time.sleep(1)
    if board.is_checkmate():
        hw.print_to_display(["Checkmate!"])
        time.sleep(1)
    if board.is_game_over():
        hw.print_to_display(["Game Over!"])
        time.sleep(1)
        board.reset()
        return State.START
    elif board.turn == chess.WHITE:
        return State.USER_MOVE
    else:
        return State.AI_MOVE
