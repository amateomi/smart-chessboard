import chess

import debug
from state.state_machine import State


def game_over_check(board: chess.Board) -> State:
    if board.is_game_over():
        print("Game over")
        board.reset()
        debug.reset_board()
        return State.START
    elif board.turn == chess.WHITE:
        return State.USER_MOVE
    else:
        return State.AI_MOVE
