import game


class Piece:

    def __init__(self, x, y, directions, player_type, state):
        self._x = x
        self._y = y
        self._directions = directions
        self._piece_type = game.PiecesTypes.NORMAL
        self._player_type = player_type
        self._state = state

        self._king = False

        if player_type == game.PlayerTypes.BOT:
            self._piece_symbol = '☻'
            self._king_symbol = '♚'
        else:
            self._piece_symbol = '☺'
            self._king_symbol = '♔'

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        if not (0 <= x <= 7):
            raise ValueError("Cannot set x of piece outside of 0-7!")
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        if not (0 <= y <= 7):
            raise ValueError("Cannot set y of piece outside of 0-7!")
        self._y = y

    @property
    def directions(self):
        return self._directions.value

    @property
    def piece_type(self):
        return self._piece_type

    def become_king(self):
        self._king = True
        self._piece_type = game.PiecesTypes.KING
        self._directions = game.Directions.ALL

    def points(self):
        if self._piece_type == game.PiecesTypes.KING:
            return 14
        else:
            if self._player_type == game.PlayerTypes.BOT:
                return 7 + self._x
            else:
                return 14 - self._x

    @property
    def piece_symbol(self):
        return self._piece_symbol

    @property
    def king_symbol(self):
        return self._king_symbol

    @property
    def king(self):
        return self._king

    @property
    def player_type(self):
        return self._player_type

    def steps(self):
        possible_moves = []
        for direction in self.directions:
            new_x, new_y = self._x + direction[0], self._y + direction[1]
            if self._state.is_inside(new_x, new_y) and self._state.board[new_x][new_y] is None:
                new_state = self.move(new_x, new_y)
                possible_moves += [new_state]
        return possible_moves

    def jumps(self):
        possible_moves = []
        for direction in self.directions:
            check_x, check_y = self._x + direction[0], self._y + direction[1]
            new_x, new_y = self._x + 2 * direction[0], self._y + 2 * direction[1]
            if self._state.is_inside(new_x, new_y) and self._state.board[new_x][new_y] is None and \
                    self._state.board[check_x][check_y] is not None:
                new_state = self.move(new_x, new_y)
                possible_moves += [new_state]
                possible_moves += self.move(new_x, new_y).board[new_x][new_y].jumps()
        return possible_moves

    def move(self, new_x, new_y):
        new_state = game.State(human_pieces=self._state.find_pieces(game.PlayerTypes.HUMAN),
                               bot_pieces=self._state.find_pieces(game.PlayerTypes.BOT))

        new_piece = Piece(new_x, new_y, self._directions, self._player_type, new_state)
        new_state.board[new_x][new_y] = new_piece
        new_state.board[self._x][self._y] = None

        if self._player_type == game.PlayerTypes.HUMAN and new_x == 0:
            new_state.board[new_x][new_y].become_king()
        if self._player_type == game.PlayerTypes.BOT and new_x == 7:
            new_state.board[new_x][new_y].become_king()

        if abs(new_x - self._x) == 2 and abs(new_y - self._y) == 2:
            enemy_x = (new_x + self._x) // 2
            enemy_y = (new_y + self._y) // 2
            if new_state.board[enemy_x][enemy_y] is not None and \
                    new_state.board[enemy_x][enemy_y].player_type != self._player_type:
                new_state.board[enemy_x][enemy_y] = None
        return new_state
