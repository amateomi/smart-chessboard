import chess

import debug
from constants import TOTAL_SQUARES

""" Represent current reed switches states:
    0 - Reed switch is open -> Square is empty
    1 - Reed switch is close -> Some piece on the square """
mask = [0] * 64

mask_stable = mask.copy()  # Store last legal mask


def update_mask():
    """ Read all board square states from MUX """
    # TODO: Read from MUX
    for i in range(TOTAL_SQUARES):
        mask[i] = debug.board[i]


def update_mask_stable():
    """ Copy mask into mask_stable """
    global mask_stable
    mask_stable = mask.copy()


def get_changed_squares() -> list[chess.Square]:
    """ Return list of squares which changed its state between current mask and mask_stable """
    return [chess.Square(i) for i in range(TOTAL_SQUARES) if mask[i] != mask_stable[i]]


def is_start_button_pressed() -> bool:
    # TODO: Add button handle
    if input("Start (y/n)?") == "y":
        return True
    else:
        return False


def is_move_button_pressed() -> bool:
    # TODO: Add button handle
    return True


def is_left_button_pressed() -> bool:
    # TODO: Add button handle
    return input("Left?") == "y"


def is_right_button_pressed() -> bool:
    # TODO: Add button handle
    return input("Right?") == "y"


def is_select_button_pressed() -> bool:
    # TODO: Add button handle
    return input("Select?") == "y"
