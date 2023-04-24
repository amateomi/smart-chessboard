import chess

board = [1] * 16 + [0] * 32 + [1] * 16


def update_board(board_to_draw: chess.Board, mask_stable: list[int]):
    global board
    board = mask_stable.copy()
    for r in range(7, -1, -1):
        print(f"\n{r + 1}", end=" ")
        for f in range(8):
            piece = board_to_draw.piece_at(chess.square(f, r))
            print(f"{piece if piece else '-'}", end=" ")
    print(f"\n  {' '.join(chess.FILE_NAMES)}")
    move = input("Enter move (a|m|e|c <source> <target> <enemy pawn spot>|<rook spot> <new rook spot>):")
    parts = move.split(" ")
    match parts[0]:
        case "a":
            board[chess.parse_square(parts[1])] = 0
        case "m":
            board[chess.parse_square(parts[1])] = 0
            board[chess.parse_square(parts[2])] = 1
        case "e":
            board[chess.parse_square(parts[1])] = 0
            board[chess.parse_square(parts[2])] = 1
            board[chess.parse_square(parts[3])] = 0
        case "c":
            board[chess.parse_square(parts[1])] = 0
            board[chess.parse_square(parts[2])] = 1
            board[chess.parse_square(parts[3])] = 0
            board[chess.parse_square(parts[4])] = 1


def pick_attacks() -> list[chess.Square]:
    return list(map(lambda x: chess.parse_square(x), input("Enter list of changed squares:").split(" ")))
