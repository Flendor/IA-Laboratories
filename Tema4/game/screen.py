import game

class Screen:
    def __init__(self):
        pass

    @staticmethod
    def widen(s):
        WIDE_MAP = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
        WIDE_MAP[0x20] = 0x3000
        return s.translate(WIDE_MAP)

    @staticmethod
    def draw(board):
        print(Screen.widen(" ABCDEFGH"))
        for line_index, board_line in enumerate(board):
            print_line = str(line_index)
            for piece_index, piece in enumerate(board_line):
                if piece is None:
                    if (piece_index + line_index) % 2 == 0:
                        print_line += 'O'
                    else:
                        print_line += '*'
                elif piece.piece_type == game.PiecesTypes.KING:
                    print_line += f'{piece.king_symbol}'
                else:
                    print_line += f'{piece.piece_symbol}'
            print(Screen.widen(print_line))
