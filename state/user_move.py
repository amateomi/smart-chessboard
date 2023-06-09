import time

import chess

import hardware_interaction as hw
from constants import TARGET_CASTLING_SQUARES
from state.select_capture import CaptureInfo
from state.state_machine import State


def user_move(board: chess.Board) -> tuple[State, chess.Move, CaptureInfo]:
    hw.print_to_display(["Make your move", "Press MOVE button"])
    if hw.is_move_button_pressed():
        hw.update_mask()
        print("Mask:")
        hw.print_mask()
        changed_squares = hw.get_changed_squares()
        print(f"Changed squares: {[chess.square_name(s) for s in changed_squares]}")
        move_or_attacked_squares = get_move_or_attacked_squares(board, changed_squares)
        if isinstance(move_or_attacked_squares, list):  # Capture
            print(f"Capture: {changed_squares[0]} -> {move_or_attacked_squares}")
            hw.update_mask_stable()
            return State.SELECT_CAPTURE, None, CaptureInfo(source_square=changed_squares[0],
                                                           attacked_squares=move_or_attacked_squares,
                                                           mask=hw.mask.copy())
        elif isinstance(move_or_attacked_squares, chess.Move):  # Move
            print(f"Move: {move_or_attacked_squares}")
            return State.MOVE_PROCESS, move_or_attacked_squares, None
        else:
            hw.print_to_display(["Unknown action"])
            time.sleep(1)
    return State.USER_MOVE, None, None


def get_move_or_attacked_squares(board: chess.Board, changed_squares: list[chess.Square]) \
        -> chess.Move:
    """ Attempts to determine the player's move based on the number of squares changed since the last mask_update.
        One changed square means that one piece captured another and stood on its square.
        Two changed squares mean the usual movement of a piece to another square.
        Three changed squares mean en passant.
        Four changed squares mean castling.
        Any other amount of changed squares are invalid. """
    changes = len(changed_squares)
    if changes == 1:
        source_square = changed_squares[0]
        if is_empty_square(source_square):
            attacked_squares = [s for s in board.attacks(source_square) if is_enemy_piece(board, s)]
            if len(attacked_squares) == 1:
                target_square = attacked_squares[0]
                return chess.Move(source_square, target_square)
            elif len(attacked_squares) > 1:
                return attacked_squares

    elif changes == 2:  # Move: source 1 -> 0, target 0 -> 1
        if is_first_empty_and_second_not_empty(changed_squares[0], changed_squares[1]):
            return chess.Move(changed_squares[0], changed_squares[1])
        elif is_first_empty_and_second_not_empty(changed_squares[1], changed_squares[0]):
            return chess.Move(changed_squares[1], changed_squares[0])

    elif changes == 3:  # En Passant: source 1 -> 0, target 0 -> 1, enemy pawn square 1 -> 0
        target_square = get_not_empty_square(changed_squares)
        if target_square:
            for square in changed_squares:
                move = chess.Move(square, target_square)
                if board.is_en_passant(move):
                    return move

    elif changes == 4:  # Castling: source 1 -> 0, target 0 -> 1, rook square 1 -> 0, new rook square 0 -> 1
        source_square = get_king_square(board, changed_squares)
        target_square = get_king_square_after_castling(changed_squares)
        if source_square and target_square:
            return chess.Move(source_square, target_square)
    return None


def is_empty_square(square: chess.Square) -> bool:
    return hw.mask[square] == 0


def is_enemy_piece(board: chess.Board, square: chess.Square) -> bool:
    return board.piece_at(square) and board.color_at(square) != board.turn


def is_first_empty_and_second_not_empty(first: chess.Square, second: chess.Square) -> bool:
    return hw.mask[first] == 0 and hw.mask[second] != 0


def get_not_empty_square(squares: list[chess.Square]) -> chess.Square:
    result = [square for square in squares if hw.mask[square] == 1]
    return result[0] if len(result) == 1 else None


def get_king_square(board: chess.Board, squares: list[chess.Square]) -> chess.Square:
    result = [square for square in squares if hw.mask[square] == 0 and board.piece_at(square).piece_type == chess.KING]
    return result[0] if len(result) == 1 else None


def get_king_square_after_castling(squares: list[chess.Square]) -> chess.Square:
    result = [square for square in squares if hw.mask[square] == 1 and square in TARGET_CASTLING_SQUARES]
    return result[0] if len(result) == 1 else None
