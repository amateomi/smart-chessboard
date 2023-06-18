from chess import parse_square, Move, Piece, QUEEN, ROOK, BISHOP, KNIGHT

TOTAL_SQUARES = 64

# All possible castling squares for the player
# NOTE: Assumed that the player always plays for the white pieces
TARGET_CASTLING_SQUARES = [parse_square("c1"),
                           parse_square("g1")]

# List of all possible player moves that may lead to pawn promotion
# NOTE: Assumed that the player always plays for the white pieces
PAWN_PROMOTION_MOVES = [Move.from_uci("a7a8"),
                        Move.from_uci("a7b8"),

                        Move.from_uci("b7a8"),
                        Move.from_uci("b7b8"),
                        Move.from_uci("b7c8"),

                        Move.from_uci("c7b8"),
                        Move.from_uci("c7c8"),
                        Move.from_uci("c7d8"),

                        Move.from_uci("d7c8"),
                        Move.from_uci("d7d8"),
                        Move.from_uci("d7e8"),

                        Move.from_uci("e7d8"),
                        Move.from_uci("e7e8"),
                        Move.from_uci("e7f8"),

                        Move.from_uci("f7e8"),
                        Move.from_uci("f7f8"),
                        Move.from_uci("f7g8"),

                        Move.from_uci("g7f8"),
                        Move.from_uci("g7g8"),
                        Move.from_uci("g7h8"),

                        Move.from_uci("h7g8"),
                        Move.from_uci("h7h8")]

PAWN_PROMOTION_STRING_OPTIONS = ["Queen", "Rook", "Bishop", "Knight"]  # Used to print options to player
PAWN_PROMOTION_OPTIONS: list[Piece] = [QUEEN, ROOK, BISHOP, KNIGHT]  # Used to set promotion for a move

PIN_MUX_OUT = 24
PINS_MUX_ADDR = [17, 27, 22, 5, 6, 13]

PIN_START_BUTTON = 14

PIN_MOVE_BUTTON = 15

PIN_SELECT_BUTTON = 16
PIN_LEFT_BUTTON = 20
PIN_RIGHT_BUTTON = 21

DISPLAY_CHANK_SIZE = 20
