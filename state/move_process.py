import chess

import hardware_interaction as hw
from constants import PAWN_PROMOTION_MOVES
from state.state_machine import State


def move_process(board: chess.Board, move: chess.Move) -> State:
    if move in PAWN_PROMOTION_MOVES:  # Only user can make moves from PAWN_PROMOTION_MOVES
        if is_valid_player_pawn_promotion(board, move):
            return State.PAWN_PROMOTION
        else:
            print(f"{move} is invalid promotion")
            return State.USER_MOVE
    elif move in board.legal_moves:
        board.push(move)
        hw.update_mask_stable()
        return State.GAME_OVER_CHECK
    else:
        print(f"{move} is invalid move")
        if board.turn == chess.BLACK:
            raise "Chess engine made invalid move"
        return State.USER_MOVE


def is_valid_player_pawn_promotion(board: chess.Board, move: chess.Move) -> bool:
    """ By default, player's move to promote pawn does not contain any particular piece to promote to.
        So we arbitrarily set promotion to queen to check move for legality (maybe player in check right now).
        Then unset promotion and return check result. """
    move.promotion = chess.QUEEN
    result = move in board.legal_moves
    move.promotion = None
    return result
