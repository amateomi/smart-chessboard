import time
from dataclasses import dataclass

import chess

import hardware_interaction as hw
from state.state_machine import State


@dataclass
class CaptureInfo:
    source_square: chess.Square  # Square from which piece capture is made
    attacked_squares: list[chess.Square]  # List of all possible attacked squares from source_square
    mask: list[int]  # Copy of the mask at the capture moment, used in capture selection algorithm


is_target_selected = False

move: chess.Move = None


def select_capture(capture_info: CaptureInfo) -> tuple[State, chess.Move]:
    global is_target_selected
    global move
    if not is_target_selected:
        hw.print_to_display(["Pick up moved piece", "Press MOVE button"])
        if hw.is_move_button_pressed():
            hw.update_mask()
            print("Mask:")
            hw.print_mask()
            changed_squares = hw.get_changed_squares()
            print(f"Changed squares: {[chess.square_name(s) for s in changed_squares]}")
            target_square = get_target_square(changed_squares, capture_info)
            if target_square:
                move = chess.Move(capture_info.source_square, target_square)
                print(f"Move: {move}")
                is_target_selected = True
            else:
                hw.print_to_display(["Invalid target"])
                time.sleep(1)
    else:
        hw.print_to_display(["Put down moved piece", "Press MOVE button"])
        if hw.is_move_button_pressed():
            hw.update_mask()
            print("Mask:")
            hw.print_mask()
            if hw.mask == capture_info.mask:
                is_target_selected = False
                return State.MOVE_PROCESS, move
            else:
                hw.print_to_display(["Different mask"])
                time.sleep(1)
    return State.SELECT_CAPTURE, None


def get_target_square(squares: list[chess.Square], capture_info: CaptureInfo) -> chess.Square:
    return squares[0] if len(squares) == 1 and squares[0] in capture_info.attacked_squares else None
