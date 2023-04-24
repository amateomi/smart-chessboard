import chess
import chess.engine

import debug
import hardware_interaction as hw
from constants import TOTAL_SQUARES
from state.state_machine import State

is_ai_made_move = False

# AI board mask. The player must repeat the move of the engine
# so that the mask after moving the pieces coincides with the AI mask
target_mask: list[int] | None = None

engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")

engine_move: chess.Move | None = None


def ai_move(board: chess.Board) -> tuple[State, chess.Move | None]:
    global is_ai_made_move
    global engine_move
    if not is_ai_made_move:
        engine_response = engine.play(board, chess.engine.Limit(time=0.5))
        engine_move = engine_response.move
        compute_target_mask(board)
        is_ai_made_move = True
    else:
        print(f"Make move {engine_move} and press move button")
        debug.update_board(board)
        if hw.is_move_button_pressed():
            hw.update_mask()
            if hw.mask == target_mask:
                is_ai_made_move = False
                return State.MOVE_PROCESS, engine_move
    return State.AI_MOVE, None


def compute_target_mask(board: chess.Board):
    """ Compute the board mask after the engine's chess move.
        The player must repeat the engine's move.
        That's why this function canceled it at the end. """
    global target_mask
    board.push(engine_move)
    target_mask = [1 if board.piece_at(square) else 0 for square in range(TOTAL_SQUARES)]
    board.pop()
