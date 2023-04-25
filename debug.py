import chess

import hardware_interaction as hw

board = [1] * 16 + [0] * 32 + [1] * 16  # Used to emulate reading from MUX


def reset_board():
    global board
    board = [1] * 16 + [0] * 32 + [1] * 16


def update_board(board_to_draw: chess.Board):
    """ Emulates the movement of pieces on the board """
    global board
    board = hw.mask_stable.copy()
    for r in range(7, -1, -1):
        print(f"\n{r + 1}", end=" ")
        for f in range(8):
            piece = board_to_draw.piece_at(chess.square(f, r))
            print(f"{piece if piece else '-'}", end=" ")
    print(f"\n  {' '.join(chess.FILE_NAMES)}")
    move = input("Enter move (a|m|e|c <source> <target> <enemy pawn spot>|<rook spot> <new rook spot>):")
    parts = move.split(" ")
    if parts[0] == "a":
        board[chess.parse_square(parts[1])] = 0
    elif parts[0] == "m":
        board[chess.parse_square(parts[1])] = 0
        board[chess.parse_square(parts[2])] = 1
    elif parts[0] == "e":
        board[chess.parse_square(parts[1])] = 0
        board[chess.parse_square(parts[2])] = 1
        board[chess.parse_square(parts[3])] = 0
    elif parts[0] == "c":
        board[chess.parse_square(parts[1])] = 0
        board[chess.parse_square(parts[2])] = 1
        board[chess.parse_square(parts[3])] = 0
        board[chess.parse_square(parts[4])] = 1


def pick_attacks() -> list[chess.Square]:
    """ Used in state.select_attack to emulate actual player actions on the board """
    return list(map(lambda x: chess.parse_square(x), input("Enter list of changed squares:").split(" ")))
