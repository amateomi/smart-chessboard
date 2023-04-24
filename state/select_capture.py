from dataclasses import dataclass

import chess

import debug
import hardware_interaction as hw
from state.state_machine import State


@dataclass
class CaptureInfo:
    source_square: chess.Square  # Square from which piece capture is made
    attacked_squares: list[chess.Square]  # List of all possible attacked squares from source_square
    mask: list[int]  # Copy of the mask at the capture moment, used in capture selection algorithm


is_target_selected = False

move: chess.Move | None = None


def select_capture(capture_info: CaptureInfo) -> tuple[State, chess.Move | None]:
    global is_target_selected
    global move
    if not is_target_selected:
        print("Pick up moved piece and press the move button")
        if hw.is_move_button_pressed():
            hw.update_mask()
            # TODO: On real board
            # changed_squares = get_changed_squares(mask, mask_stable)
            changed_squares = debug.pick_attacks()
            print(changed_squares)
            target_square = get_target_square(changed_squares, capture_info)
            if target_square:
                move = chess.Move(capture_info.source_square, target_square)
                is_target_selected = True
    else:
        print("Put down moved piece and press the move button")
        if hw.is_move_button_pressed():
            hw.update_mask()
            if hw.mask == capture_info.mask:
                is_target_selected = False
                return State.MOVE_PROCESS, move
    return State.SELECT_CAPTURE, None


def get_target_square(squares: list[chess.Square], capture_info: CaptureInfo) -> chess.Square | None:
    return squares[0] if len(squares) == 1 and squares[0] in capture_info.attacked_squares else None
