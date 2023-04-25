import chess

from state.ai_move import ai_move
from state.game_over_check import game_over_check
from state.move_process import move_process
from state.pawn_promotion import pawn_promotion
from state.select_capture import select_capture, CaptureInfo
from state.start import start
from state.state_machine import State
from state.user_move import user_move


def main():
    move: chess.Move = None
    capture_info: CaptureInfo = None
    board = chess.Board()
    state = State.START
    while True:
        if state == State.START:
            state = start()

        elif state == State.USER_MOVE:
            state, move, capture_info = user_move(board)

        elif state == State.AI_MOVE:
            state, move = ai_move(board)

        elif state == State.SELECT_CAPTURE:
            state, move = select_capture(capture_info)

        elif state == State.MOVE_PROCESS:
            state = move_process(board, move)

        elif state == State.PAWN_PROMOTION:
            state, move = pawn_promotion(move)

        elif state == State.GAME_OVER_CHECK:
            state = game_over_check(board)


if __name__ == "__main__":
    main()
