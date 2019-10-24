import game


class HumanStrategy:

    @staticmethod
    def syntactic_check(position):
        while len(position) != 2 or not position[0].isdigit() or not position[1].isalpha():
            position = input("Invalid position! Please try again!")
        return int(position[0]), ord(position[1]) - ord('A')

    @staticmethod
    def play(state):

        current_position = input("What piece do you want to move? ")
        current_position = HumanStrategy.syntactic_check(current_position)

        human_pieces = state.find_pieces(game.PlayerTypes.HUMAN)
        human_pieces_x = [piece.x for piece in human_pieces]
        human_pieces_y = [piece.y for piece in human_pieces]
        while (current_position[0], current_position[1]) not in zip(human_pieces_x, human_pieces_y):
            current_position = input("Invalid position! Please try again! ")
            current_position = HumanStrategy.syntactic_check(current_position)

        next_position = input("Where do you want to move it? ")
        next_position = HumanStrategy.syntactic_check(next_position)

        bot_pieces = state.find_pieces(game.PlayerTypes.BOT)
        bot_pieces_x = [piece.x for piece in bot_pieces]
        bot_pieces_y = [piece.y for piece in bot_pieces]
        while (next_position[0], next_position[1]) in zip(human_pieces_x, human_pieces_y) or \
                (next_position[0], next_position[1]) in zip(bot_pieces_x, bot_pieces_y):
            next_position = input("Invalid position! Please try again! ")
            next_position = HumanStrategy.syntactic_check(next_position)

        for piece in human_pieces:
            if piece.x == current_position[0] and piece.y == current_position[1]:
                possible_states = piece.steps() + piece.jumps()
                for possible_state in possible_states:
                    if possible_state.board[next_position[0]][next_position[1]] is not None and \
                            possible_state.board[current_position[0]][current_position[1]] is None:
                        return possible_state
        print('Move not allowed!')
        return HumanStrategy.play(state)
