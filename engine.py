import enum

import chess

TOTAL_SQUARES = 64

State = enum.Enum(
    value="ApplicationState",
    names=("start", "user_move", "select_attack", "move_process")
)

# TODO: Move to main function
board = chess.Board()

debug_board = [1] * 16 + [0] * 32 + [1] * 16
debug_board_unstable = debug_board.copy()


def init_masks() -> (list[int], list[int]):
    """ Represent current reed switch states
    0 - Reed is open -> Square is empty
    1 - Reed is close -> Some piece on the square """
    mask = [0] * 64
    mask_prev = mask.copy()  # Previous mask state
    return mask, mask_prev


def update_mask(mask: list[int]):
    # TODO: Read from MUX
    for i in range(TOTAL_SQUARES):
        mask[i] = debug_board_unstable[i]


def is_start_button_pressed() -> bool:
    # TODO: Add button handle
    if input("Start (y/n)?") == "y":
        return True
    else:
        return False


def debug_update_board():
    global debug_board_unstable
    debug_board_unstable = debug_board.copy()
    for r in range(7, -1, -1):
        print(f"\n{r + 1}", end=" ")
        for f in range(8):
            piece = board.piece_at(chess.square(f, r))
            print(f"{piece if piece else '-'}", end=" ")
    print(f"\n  {' '.join(chess.FILE_NAMES)}")
    move = input("Enter move (a|m|e|c <source> <target> <enemy pawn spot>|<rook spot> <new rook spot>):")
    parts = move.split(" ")
    match parts[0]:
        case "a":
            debug_board_unstable[chess.parse_square(parts[1])] = 0
        case "m":
            debug_board_unstable[chess.parse_square(parts[1])] = 0
            debug_board_unstable[chess.parse_square(parts[2])] = 1
        case "e":
            debug_board_unstable[chess.parse_square(parts[1])] = 0
            debug_board_unstable[chess.parse_square(parts[2])] = 1
            debug_board_unstable[chess.parse_square(parts[3])] = 0
        case "c":
            debug_board_unstable[chess.parse_square(parts[1])] = 0
            debug_board_unstable[chess.parse_square(parts[2])] = 1
            debug_board_unstable[chess.parse_square(parts[3])] = 0
            debug_board_unstable[chess.parse_square(parts[4])] = 1


def debug_attack_pick() -> list[chess.Square]:
    return list(map(lambda x: chess.parse_square(x), input("Enter list of changed squares:").split(" ")))


def is_good_start_position(mask: list[int]) -> bool:
    for i in range(TOTAL_SQUARES):
        if 16 <= i < 48 and mask[i] or not 16 <= i < 48 and not mask[i]:
            return False
    return True


def is_move_button_pressed() -> bool:
    # TODO: Add button handle
    return True


def get_changed_squares(mask: list[int], mask_prev: list[int]) -> list[chess.Square]:
    return [chess.Square(i) for i in filter(lambda i: mask[i] != mask_prev[i], range(TOTAL_SQUARES))]


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


def main():
    global debug_board
    move_selected = False

    mask, mask_prev = init_masks()
    state = State.start
    while True:
        match state:
            case State.start:
                if is_start_button_pressed():
                    update_mask(mask)
                if is_good_start_position(mask):
                    mask_prev = mask.copy()
                    state = State.user_move

            case State.user_move:
                debug_update_board()

                if is_move_button_pressed():
                    update_mask(mask)
                    changed_squares = get_changed_squares(mask, mask_prev)
                    print(changed_squares)
                    move_or_attack_list = get_chess_move_or_attack_list(mask, changed_squares)
                    if isinstance(move_or_attack_list, list):
                        attack_mask = mask.copy()
                        attack_source = changed_squares[0]
                        attacks = move_or_attack_list
                        print(f"{attack_source} -> {attacks}")
                        state = State.select_attack
                    else:
                        move = move_or_attack_list
                        if move and move in board.legal_moves:
                            board.push(move)
                            debug_board = debug_board_unstable.copy()
                            mask_prev = mask.copy()
                        else:
                            print(f"{move} is invalid")

            case State.select_attack:
                if not move_selected:
                    print("Pick up the moved piece and press the move button")
                    if is_move_button_pressed():
                        update_mask(mask)
                        # On real board
                        # changed_squares = get_changed_squares(mask, mask_prev)
                        changed_squares = debug_attack_pick()
                        if len(changed_squares) == 1 and changed_squares[0] in attacks:
                            move = chess.Move(attack_source, changed_squares[0])
                            move_selected = True
                else:
                    print("Put down the moved piece and press the move button")
                    if is_move_button_pressed():
                        update_mask(mask)
                        if mask == attack_mask:
                            move_selected = False
                            state = State.move_process

            case State.move_process:
                if move and move in board.legal_moves:
                    board.push(move)
                    debug_board = debug_board_unstable.copy()
                    mask_prev = mask.copy()
                else:
                    print(f"{move} is invalid")
                state = State.user_move


if __name__ == "__main__":
    main()
