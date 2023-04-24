import hardware_interaction as hw

from constants import TOTAL_SQUARES
from state.state_machine import State


def start():
    if hw.is_start_button_pressed():
        hw.update_mask()
    if is_good_start_position():
        hw.update_mask_stable()
        return State.USER_MOVE
    return State.START


def is_good_start_position() -> bool:
    for i in range(TOTAL_SQUARES):
        if 16 <= i < 48 and hw.mask[i] == 1 or not 16 <= i < 48 and hw.mask[i] == 0:
            return False
    return True
