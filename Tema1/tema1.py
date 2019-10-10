def initialize(boat_capacity, number_of_missionaries, number_of_cannibals):
    return {
        "boat": {"capacity": boat_capacity,
                 "position": 0},
        "number_of_missionaries": [number_of_missionaries,0],
        "number_of_cannibals": [number_of_cannibals,0]
    }


def is_final(state):
    return (state["number_of_missionaries"][0] == 0 and
            state["number_of_cannibals"][0] == 0 and
            state["boat"]["position"] == 1 and
            state["number_of_missionaries"][1] > 0 and
            state["number_of_cannibals"][1] > 0)


def transition(state, moved_missionaries, moved_cannibals, to):
    state["boat"]["position"] = to

    if to == 1:

        state["number_of_missionaries"][1] += moved_missionaries
        state["number_of_missionaries"][0] -= moved_missionaries

        state["number_of_cannibals"][1] += moved_cannibals
        state["number_of_cannibals"][0] -= moved_cannibals
        return state

    state["number_of_missionaries"][0] += moved_missionaries
    state["number_of_missionaries"][1] -= moved_missionaries

    state["number_of_cannibals"][0] += moved_cannibals
    state["number_of_cannibals"][1] -= moved_cannibals
    return state


def validation(state, moved_missionaries, moved_cannibals):
    return (state["number_of_missionaries"][0] > 0 and state["number_of_missionaries"][0] >= state["number_of_cannibals"][0] and
            state["number_of_missionaries"][1] > 0 and state["number_of_missionaries"][1] >= state["number_of_cannibals"][1] and
            moved_missionaries >= 0 and moved_cannibals >= 0 and 0 < moved_cannibals + moved_missionaries <= state["boat"]["capacity"])


def strategy(state, strategy_name = "random"):
    if strategy_name not in ["random", "bkt", "iddfs"]:
        return None

    to = state["boat"]["position"]
    while not is_final(state):
        to = 1 - to
        if strategy_name == "random":
            # Choose random moved_missionaries, moved_cannibals from possible transitions
        elif strategy_name == "bkt":
            # Choose bkt moved_missionaries, moved_cannibals from possible transitions
        elif strategy_name == "iddfs":
            # Choose iddfs moved_missionaries, moved_cannibals from possible transitions
        new_state = transition(state, moved_missionaries, moved_cannibals, to)
        if validation(new_state, moved_missionaries, moved_cannibals):
            state = new_state

    return state


print(initialize(3, 5, 5))