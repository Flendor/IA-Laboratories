import random


def initialize(boat_capacity, number_of_missionaries, number_of_cannibals):
    return {
        "boat": {"capacity": boat_capacity,
                 "position": 0},
        "number_of_missionaries": [number_of_missionaries, 0],
        "number_of_cannibals": [number_of_cannibals, 0]
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


def validation(state, moved_missionaries, moved_cannibals, to):
    return (state["number_of_missionaries"][0] + ((-1)** to) * moved_missionaries >= state["number_of_cannibals"][0] + ((-1)** to) * moved_cannibals and
            state["number_of_missionaries"][1] + ((-1)** to) * moved_missionaries >= state["number_of_cannibals"][1] + ((-1)** to) * moved_cannibals and
            moved_missionaries >= 0 and moved_cannibals >= 0 and 0 < moved_cannibals + moved_missionaries <= state["boat"]["capacity"] and
            state["number_of_missionaries"][1 - to] - moved_missionaries >= 0 and state["number_of_cannibals"][1 - to] - moved_cannibals >= 0)


def random_strategy(state):
    counter_init = 100
    state_init = state

    to = state["boat"]["position"]

    counter = counter_init
    visited_states = []

    while not is_final(state):
        to = 1 - to
        moved_missionaries = random.randint(0, state["number_of_missionaries"][1 - to])
        moved_cannibals = random.randint(0, state["number_of_cannibals"][1 - to])
        new_state = transition(state, moved_missionaries, moved_cannibals, to)

        if new_state not in visited_states and validation(new_state, moved_missionaries, moved_cannibals):
            state = new_state
            visited_states.append(state)


        print(state)

        counter -= 1
        if counter == 0:
            counter = counter_init
            visited_states = []
            state = state_init

    return state


# def bkt_strategy(state):
#     to = state["boat"]["position"]
#     while not is_final(state):
#         to = 1 - to
#         # Choose bkt moved_missionaries, moved_cannibals from possible transitions
#         new_state = transition(state, moved_missionaries, moved_cannibals, to)
#         if validation(state, moved_missionaries, moved_cannibals):
#             state = transition(state, moved_missionaries, moved_cannibals, to)
#
#     return state
#
#
# def iddfs_strategy(state):
#     to = state["boat"]["position"]
#     while not is_final(state):
#         to = 1 - to
#         # Choose iddfs moved_missionaries, moved_cannibals from possible transitions
#         new_state = transition(state, moved_missionaries, moved_cannibals, to)
#         if validation(new_state, moved_missionaries, moved_cannibals):
#             state = new_state
#
#     return state

def bkt(state, k, visited_states):
    for i in range(0, state["number_of_missionaries"][1 - to]):
        for j in range(0, state["number_of_cannibals"][1 - to]):
            if validation(state, i, j, to):
                state = transition(state, i, j, to)
                if len(visited_states) < k:
                    visited_states.append(state)
                else:
                    visited_states[k] = state
                if is_final(state):
                    


# print(initialize(3, 5, 5))
