import game


class State:
    __initial_human_pieces_positions = [(7, 0), (6, 1), (7, 2), (6, 3), (7, 4), (6, 5), (7, 6), (6, 7), (5, 0), (5, 2),
                                        (5, 4), (5, 6)]
    __initial_bot_pieces_positions = [(1, 0), (0, 1), (1, 2), (0, 3), (1, 4), (0, 5), (1, 6), (0, 7), (2, 1), (2, 3),
                                      (2, 5), (2, 7)]

    def __init__(self,
                 human_pieces=None,
                 bot_pieces=None):
        self._board = [[None] * 8, [None] * 8, [None] * 8, [None] * 8, [None] * 8, [None] * 8, [None] * 8, [None] * 8]
        if human_pieces is None:
            _human_pieces = [
                game.Piece(x=x, y=y, piece_type=game.PiecesTypes.NORMAL, directions=game.Directions.HUMAN,
                           player_type=game.PlayerTypes.HUMAN, state=self)
                for
                x, y in self.__initial_human_pieces_positions]
        else:
            _human_pieces = [game.Piece(x=human_piece.x, y=human_piece.y, piece_type=human_piece.piece_type,
                                        directions=human_piece.directions,
                                        player_type=game.PlayerTypes.HUMAN, state=self)
                             for
                             human_piece in human_pieces]

        if bot_pieces is None:
            _bot_pieces = [
                game.Piece(x=x, y=y, piece_type=game.PiecesTypes.NORMAL, directions=game.Directions.BOT,
                           player_type=game.PlayerTypes.BOT, state=self)
                for
                x, y in self.__initial_bot_pieces_positions]
        else:
            _bot_pieces = [game.Piece(x=bot_piece.x, y=bot_piece.y, piece_type=bot_piece.piece_type,
                                      directions=bot_piece.directions,
                                      player_type=game.PlayerTypes.BOT, state=self)
                           for
                           bot_piece in bot_pieces]

        for piece in _human_pieces:
            self._board[piece.x][piece.y] = piece

        for piece in _bot_pieces:
            self._board[piece.x][piece.y] = piece

    def find_pieces(self, player_type):
        my_pieces = []
        for i in range(0, 8):
            for j in range(0, 8):
                if isinstance(self._board[i][j], game.Piece):
                    if self._board[i][j].player_type == player_type:
                        my_pieces += [self._board[i][j]]
        return my_pieces

    def lost(self, player_type):
        if len(self.find_pieces(player_type)) == 0:
            return True
        for piece in self.find_pieces(player_type):
            for direction in piece.directions.value:
                if piece.steps() != [] or piece.jumps() != []:
                    return False
        return True

    def get_winner(self):
        if self.lost(game.PlayerTypes.HUMAN):
            return game.PlayerTypes.BOT
        if self.lost(game.PlayerTypes.BOT):
            return game.PlayerTypes.HUMAN
        return None

    @property
    def board(self):
        return self._board

    @staticmethod
    def is_inside(x, y):
        return 0 <= x <= 7 and 0 <= y <= 7

    def score(self):
        bot_sum = 0
        human_sum = 0
        bot_pieces = self.find_pieces(game.PlayerTypes.BOT)
        human_pieces = self.find_pieces(game.PlayerTypes.HUMAN)

        for bot_piece in bot_pieces:
            bot_sum += bot_piece.points()

        for human_piece in human_pieces:
            human_sum += human_piece.points()

        return bot_sum - human_sum
