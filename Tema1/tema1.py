import random
import copy


######################################### Functions for states #########################################

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
            state["number_of_missionaries"][1] >= 0 and
            state["number_of_cannibals"][1] >= 0)


def transition(state, moved_missionaries, moved_cannibals, to):
    transitioned_state = copy.deepcopy(state)
    transitioned_state["boat"]["position"] = to

    if to == 1:
        transitioned_state["number_of_missionaries"][1] += moved_missionaries
        transitioned_state["number_of_missionaries"][0] -= moved_missionaries

        transitioned_state["number_of_cannibals"][1] += moved_cannibals
        transitioned_state["number_of_cannibals"][0] -= moved_cannibals
        return transitioned_state

    transitioned_state["number_of_missionaries"][0] += moved_missionaries
    transitioned_state["number_of_missionaries"][1] -= moved_missionaries

    transitioned_state["number_of_cannibals"][0] += moved_cannibals
    transitioned_state["number_of_cannibals"][1] -= moved_cannibals
    return transitioned_state


def validation(state, moved_missionaries, moved_cannibals, to):
    return ((state["number_of_missionaries"][0] + ((-1) ** to) * moved_missionaries == 0 or
             state["number_of_missionaries"][0] + ((-1) ** to) * moved_missionaries >= state["number_of_cannibals"][
                 0] + ((-1) ** to) * moved_cannibals) and
            (state["number_of_missionaries"][1] + ((-1) ** (1 - to)) * moved_missionaries == 0 or
             state["number_of_missionaries"][1] + ((-1) ** (1 - to)) * moved_missionaries >=
             state["number_of_cannibals"][1] + ((-1) ** (1 - to)) * moved_cannibals) and
            moved_missionaries >= 0 and moved_cannibals >= 0 and 0 < moved_cannibals + moved_missionaries <=
            state["boat"]["capacity"] and
            state["number_of_missionaries"][1 - to] - moved_missionaries >= 0 and state["number_of_cannibals"][
                1 - to] - moved_cannibals >= 0)


######################################### Strategies #########################################


#################### Random ####################

def random_strategy(state):
    counter_init = 100
    state_init = copy.deepcopy(state)

    counter = counter_init
    visited_states = [copy.deepcopy(state_init)]

    while not is_final(state):
        to = 1 - state["boat"]["position"]

        moved_missionaries = random.randint(0, state["number_of_missionaries"][1 - to])
        moved_cannibals = random.randint(0, state["number_of_cannibals"][1 - to])

        if validation(state, moved_missionaries, moved_cannibals, to):
            new_state = transition(state, moved_missionaries, moved_cannibals, to)
            if new_state not in visited_states:
                state = new_state
                visited_states.append(state)

        counter -= 1
        if counter == 0:
            counter = counter_init
            visited_states = [copy.deepcopy(state_init)]
            state = copy.deepcopy(state_init)

    for visited_state in visited_states:
        print(visited_state)

    return len(visited_states) - 1


#################### iIDDFS ####################

def iddfs_strategy(state):
    state_init = copy.deepcopy(state)

    stack_of_states = [(state_init, 1, [state_init])]
    last_row = stack_of_states[:]
    state, current_level, history_of_states = stack_of_states.pop()
    maximum_allowed_depth = 1
    visited_states = [state_init]

    while not is_final(state):
        to = 1 - state["boat"]["position"]

        for moved_missionaries in range(state["number_of_missionaries"][1 - to], -1, -1):
            for moved_cannibals in range(state["number_of_cannibals"][1 - to], -1, -1):
                if validation(state, moved_missionaries, moved_cannibals,
                              to) and current_level + 1 <= maximum_allowed_depth:
                    new_state = transition(state, moved_missionaries, moved_cannibals, to)
                    if new_state not in visited_states:
                        stack_of_states.append((new_state, current_level + 1, history_of_states + [new_state]))
                        visited_states.append(new_state)
                        if current_level + 1 == maximum_allowed_depth:
                            last_row.append((new_state, current_level + 1, history_of_states + [new_state]))

        if len(stack_of_states) == 0:
            maximum_allowed_depth += 1
            stack_of_states = last_row[:]
            last_row = []

        if len(stack_of_states) == 0:
            return None

        state, current_level, history_of_states = stack_of_states.pop()

    for state_from_path in history_of_states:
        print(state_from_path)

    return len(history_of_states) - 1


#################### BKT ####################

bkt_flag = False


def bkt(state, visited_states, to):
    global bkt_flag
    bkt_return = 0
    if bkt_flag:
        return bkt_return
    for moved_missionaries in range(state["number_of_missionaries"][1 - to] + 1):
        for moved_cannibals in range(state["number_of_cannibals"][1 - to] + 1):
            if validation(state, moved_missionaries, moved_cannibals, to):
                new_state = transition(state, moved_missionaries, moved_cannibals, to)
                if new_state not in visited_states:
                    visited_states.append(new_state)
                    if is_final(new_state):
                        for v in visited_states:
                            print(v)
                        bkt_flag = True
                        return len(visited_states) - 1
                    else:
                        bkt_return = bkt(new_state, visited_states, 1 - to)
                    if bkt_flag:
                        return bkt_return
                    visited_states.pop()


def bkt_strategy(state):
    return bkt(state, [state], 1)


# print(random_strategy(initialize(4, 10, 10)))
print(iddfs_strategy(initialize(4, 10, 10)))
print(bkt_strategy(initialize(4, 10, 10)))
