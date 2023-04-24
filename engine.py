from enum import Enum

import chess
import chess.engine

import debug

TOTAL_SQUARES = 64

""" List of all possible user moves that may lead to pawn promotion """
PAWN_PROMOTION_MOVES = [chess.Move.from_uci("a7a8"),
                        chess.Move.from_uci("a7b8"),

                        chess.Move.from_uci("b7a8"),
                        chess.Move.from_uci("b7b8"),
                        chess.Move.from_uci("b7c8"),

                        chess.Move.from_uci("c7b8"),
                        chess.Move.from_uci("c7c8"),
                        chess.Move.from_uci("c7d8"),

                        chess.Move.from_uci("d7c8"),
                        chess.Move.from_uci("d7d8"),
                        chess.Move.from_uci("d7e8"),

                        chess.Move.from_uci("e7d8"),
                        chess.Move.from_uci("e7e8"),
                        chess.Move.from_uci("e7f8"),

                        chess.Move.from_uci("f7e8"),
                        chess.Move.from_uci("f7f8"),
                        chess.Move.from_uci("f7g8"),

                        chess.Move.from_uci("g7f8"),
                        chess.Move.from_uci("g7g8"),
                        chess.Move.from_uci("g7h8"),

                        chess.Move.from_uci("h7g8"),
                        chess.Move.from_uci("h7h8")]

PAWN_PROMOTION_OPTIONS = ["Queen", "Rook", "Bishop", "Knight"]
PAWN_PROMOTION_CHARACTERS = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
pawn_promotion_index = 0

# TODO: Move to main function
board = chess.Board()


def init_masks() -> (list[int], list[int]):
    """ Represent current reed switch states
    0 - Reed is open -> Square is empty
    1 - Reed is close -> Some piece on the square """
    mask = [0] * 64
    mask_stable = mask.copy()  # Store last legal board state
    return mask, mask_stable


def update_mask(mask: list[int]):
    # TODO: Read from MUX
    for i in range(TOTAL_SQUARES):
        mask[i] = debug.board[i]


def is_start_button_pressed() -> bool:
    # TODO: Add button handle
    if input("Start (y/n)?") == "y":
        return True
    else:
        return False


def is_good_start_position(mask: list[int]) -> bool:
    for i in range(TOTAL_SQUARES):
        if 16 <= i < 48 and mask[i] or not 16 <= i < 48 and not mask[i]:
            return False
    return True


def is_move_button_pressed() -> bool:
    # TODO: Add button handle
    return True


def get_changed_squares(mask: list[int], mask_stable: list[int]) -> list[chess.Square]:
    return [chess.Square(i) for i in filter(lambda i: mask[i] != mask_stable[i], range(TOTAL_SQUARES))]


def is_left_button_pressed() -> bool:
    return input("Left?") == "y"


def is_right_button_pressed() -> bool:
    return input("Right?") == "y"


def is_select_button_pressed() -> bool:
    return input("Select?") == "y"


def get_chess_move_or_attack_list(mask: list[int], changed_squares: list[chess.Square]) \
        -> chess.Move | list[chess.Square] | None:
    match len(changed_squares):
        case 1:
            # Attack: source 1 -> 0
            if not mask[changed_squares[0]]:
                possible_attacked_squares = board.attacks(changed_squares[0])
                possible_attacked_squares = list(
                    filter(lambda s: board.piece_at(s) and board.color_at(s) != board.turn, possible_attacked_squares))
                if len(possible_attacked_squares) == 1:
                    return chess.Move(changed_squares[0], possible_attacked_squares.pop())
                else:
                    return possible_attacked_squares

        case 2:
            # Move: source 1 -> 0, target 0 -> 1
            if not mask[changed_squares[0]] and mask[changed_squares[1]]:
                return chess.Move(changed_squares[0], changed_squares[1])
            elif not mask[changed_squares[1]] and mask[changed_squares[0]]:
                return chess.Move(changed_squares[1], changed_squares[0])

        case 3:
            # En Passant: source 1 -> 0, target 0 -> 1, enemy pawn spot 1 -> 0
            target = filter(lambda s: mask[s], changed_squares)
            if not target:
                return None
            target = next(target)

            for source in changed_squares:
                if not mask[source]:
                    move = chess.Move(source, target)
                    if board.is_en_passant(move):
                        return move

        case 4:
            # Castling: source 1 -> 0, target 0 -> 1, rook spot 1 -> 0, new rook spot 0 -> 1
            source = filter(lambda s: not mask[s] and board.piece_at(s).piece_type == chess.KING, changed_squares)
            if not source:
                return None
            source = next(source)
            target = filter(lambda s: mask[s] and s in [2, 6, 58, 62], changed_squares)
            if not target:
                return None
            target = next(target)
            return chess.Move(source, target)
    return None


class State(Enum):
    START = 1
    USER_MOVE = 2
    AI_MOVE = 3
    SELECT_ATTACK = 4
    MOVE_PROCESS = 5
    PAWN_PROMOTION = 6
    GAME_OVER_CHECK = 7


def main():
    state = State.START

    global pawn_promotion_index

    move = None
    is_ai_made_move = None
    right_mask = None
    attack_mask = None
    attack_source = None
    attacks = None
    move_selected = None

    engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")

    mask, mask_stable = init_masks()
    while True:
        match state:
            case State.START:
                if is_start_button_pressed():
                    update_mask(mask)
                if is_good_start_position(mask):
                    mask_stable = mask.copy()
                    state = State.USER_MOVE

            case State.USER_MOVE:
                debug.update_board(board, mask_stable)

                if is_move_button_pressed():
                    update_mask(mask)
                    changed_squares = get_changed_squares(mask, mask_stable)
                    print(changed_squares)
                    move_or_attack_list = get_chess_move_or_attack_list(mask, changed_squares)
                    if isinstance(move_or_attack_list, list) and move_or_attack_list:
                        attacks = move_or_attack_list
                        attack_source = changed_squares[0]
                        attack_mask = mask.copy()
                        print(f"{attack_source} -> {attacks}")
                        state = State.SELECT_ATTACK
                    else:
                        move = move_or_attack_list
                        state = State.MOVE_PROCESS

            case State.AI_MOVE:
                if not is_ai_made_move:
                    engine_response = engine.play(board, chess.engine.Limit(time=0.5))
                    move = engine_response.move
                    # move = chess.Move.from_uci(input("Enter ai move:"))
                    board.push(move)
                    right_mask = [1 if board.piece_at(i) else 0 for i in range(TOTAL_SQUARES)]
                    board.pop()
                    is_ai_made_move = True
                else:
                    print(f"Make move {move} and press move button")
                    debug.update_board(board, mask_stable)
                    if is_move_button_pressed():
                        update_mask(mask)
                        if mask == right_mask:
                            is_ai_made_move = False
                            state = State.MOVE_PROCESS

            case State.SELECT_ATTACK:
                if not move_selected:
                    print("Pick up moved piece and press the move button")
                    if is_move_button_pressed():
                        update_mask(mask)
                        # On real board
                        # changed_squares = get_changed_squares(mask, mask_stable)
                        changed_squares = debug.pick_attacks()
                        if len(changed_squares) == 1 and changed_squares[0] in attacks:
                            move = chess.Move(attack_source, changed_squares[0])
                            move_selected = True
                else:
                    print("Put down moved piece and press the move button")
                    if is_move_button_pressed():
                        update_mask(mask)
                        if mask == attack_mask:
                            move_selected = False
                            state = State.MOVE_PROCESS

            case State.MOVE_PROCESS:
                if move in PAWN_PROMOTION_MOVES:  # Only user can make move from PAWN_PROMOTION_MOVES
                    move.promotion = chess.QUEEN  # Reason: board.legal_moves not contain PAWN_PROMOTION_MOVES
                    is_valid_promotion = move in board.legal_moves
                    move.promotion = None
                    if is_valid_promotion:
                        state = state.pawn_promotion
                    else:
                        print(f"{move} is invalid promotion")
                        state = State.USER_MOVE
                elif move in board.legal_moves:
                    board.push(move)
                    mask_stable = mask.copy()
                    state = State.GAME_OVER_CHECK
                else:
                    print(f"{move} is invalid move")
                    if board.turn == chess.BLACK:
                        raise "Chess engine made invalid move"
                    state = State.USER_MOVE

            case State.PAWN_PROMOTION:
                print(f"Select piece {PAWN_PROMOTION_OPTIONS[pawn_promotion_index]}?")
                if is_select_button_pressed():
                    move.promotion = PAWN_PROMOTION_CHARACTERS[pawn_promotion_index]
                    state = State.MOVE_PROCESS
                elif is_left_button_pressed() and pawn_promotion_index > 0:
                    pawn_promotion_index -= 1
                elif is_right_button_pressed() and pawn_promotion_index < len(PAWN_PROMOTION_OPTIONS) - 1:
                    pawn_promotion_index += 1

            case State.GAME_OVER_CHECK:
                if board.is_game_over():
                    print("Game over")
                    board.reset()
                    debug.board = mask_stable.copy()
                    state = State.START
                elif board.turn == chess.WHITE:
                    state = State.USER_MOVE
                else:
                    state = State.AI_MOVE


if __name__ == "__main__":
    main()
