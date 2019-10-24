import game


class BotStrategy:
    @staticmethod
    def states_after_bot_moved(state):
        states = []
        pieces = state.find_pieces(game.PlayerTypes.BOT)
        for piece in pieces:
            states += piece.steps()
            states += piece.jumps()
        return states

    @staticmethod
    def states_after_human_moved(state):
        states = []
        pieces = state.find_pieces(game.PlayerTypes.HUMAN)
        for piece in pieces:
            states += piece.steps()
            states += piece.jumps()
        return states

    @staticmethod
    def min_max(state, look_ahead=2):
        if look_ahead <= 0:
            return state, state.score()

        max_layer = BotStrategy.states_after_bot_moved(state)
        max_layer_score = -(12 * 14)
        selected_state = None

        for max_layer_state in max_layer:
            min_layer = BotStrategy.states_after_human_moved(max_layer_state)
            min_layer_score = 12 * 14

            for min_layer_state in min_layer:
                recursive_state, recursive_state_score = BotStrategy.min_max(min_layer_state, look_ahead - 1)

                if min_layer_score is None or recursive_state_score < min_layer_score:
                    min_layer_score = recursive_state_score

            if max_layer_score is None or min_layer_score > max_layer_score:
                max_layer_score = min_layer_score
                selected_state = max_layer_state

        return selected_state, max_layer_score

    @staticmethod
    def alpha_beta(state):
        pass
