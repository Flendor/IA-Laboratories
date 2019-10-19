import random
import copy
from timeit import default_timer as timer
import sys


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
    counter_init = 1000
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


def bkt(state, visited_states, all_bkt_states, to):
    global bkt_flag
    bkt_return = 0
    if bkt_flag:
        return bkt_return
    for moved_missionaries in range(state["number_of_missionaries"][1 - to] + 1):
        for moved_cannibals in range(state["number_of_cannibals"][1 - to] + 1):
            if validation(state, moved_missionaries, moved_cannibals, to):
                new_state = transition(state, moved_missionaries, moved_cannibals, to)
                if new_state not in all_bkt_states:
                    visited_states.append(new_state)
                    all_bkt_states.append(new_state)
                    if is_final(new_state):
                        for v in visited_states:
                            print(v)
                        bkt_flag = True
                        return len(visited_states) - 1
                    else:
                        bkt_return = bkt(new_state, visited_states, all_bkt_states, 1 - to)
                    if bkt_flag:
                        return bkt_return
                    visited_states.pop()


def bkt_strategy(state):
    return bkt(state, [state], [state], 1)


#################### A* ####################

def number_of_people_on_the_first_shore(state):
    return state['number_of_missionaries'][0] + state['number_of_cannibals'][0] + state['boat']['position']


def heuristic_distance(state):
    return number_of_people_on_the_first_shore(state)


def a_star(initial_state):
    distance = {str(initial_state): 0}
    parent = {str(initial_state): None}
    queue = [initial_state]

    while len(queue) > 0:
        state = queue.pop()
        to = 1 - state["boat"]["position"]

        if is_final(state):
            path = [state]
            while parent[str(state)] is not None:
                state = parent[str(state)]
                path += [state]

            for state in reversed(path):
                print(state)
            return len(path) - 1

        for moved_missionaries in range(state["number_of_missionaries"][1 - to], -1, -1):
            for moved_cannibals in range(state["number_of_cannibals"][1 - to], -1, -1):
                if validation(state, moved_missionaries, moved_cannibals, to):
                    new_state = transition(state, moved_missionaries, moved_cannibals, to)
                    if str(new_state) in distance.keys() and distance[str(state)] + 1 < distance[str(new_state)]:
                        distance[str(new_state)] = distance[str(state)] + 1
                        parent[str(new_state)] = state
                        queue.append(new_state)
                    elif str(new_state) not in distance.keys():
                        distance[str(new_state)] = distance[str(state)] + 1
                        parent[str(new_state)] = state
                        queue.append(new_state)

        queue.sort(reverse=True,
                   key=lambda current_state: distance[str(current_state)] + heuristic_distance(current_state))


def generate_one_instance():
    return random.randrange(2, 5), random.randrange(3, 15), random.randrange(3, 15)


def generate_all_instances():
    instances = []
    for i in range(0, 10):
        current_instance = generate_one_instance()
        while current_instance in instances or \
                not a_star(initialize(current_instance[0], current_instance[1], current_instance[2])):
            current_instance = generate_one_instance()
        instances.append(current_instance)
    return instances


def run_one_time(alg, file, instance, stats):
    if alg == "A*":
        alg_start = timer()
        alg_length = a_star(initialize(instance[0], instance[1], instance[2]))
        alg_end = timer()
    elif alg == "IDDFS":
        alg_start = timer()
        alg_length = iddfs_strategy(initialize(instance[0], instance[1], instance[2]))
        alg_end = timer()
    elif alg == "BKT":
        alg_start = timer()
        alg_length = bkt_strategy(initialize(instance[0], instance[1], instance[2]))
        alg_end = timer()
    else:
        alg_start = timer()
        alg_length = random_strategy(initialize(instance[0], instance[1], instance[2]))
        alg_end = timer()
    stats[0].append(alg_length)
    stats[1].append(round(alg_end - alg_start, 4))
    file.write(alg + ": solution of " + str(stats[0][len(stats[0]) - 1]) +
               " states and a duration of " + str(stats[1][len(stats[1]) - 1]) +
               '\n')


def run_instances(instances):
    global bkt_flag
    a_star_stats = ([], [])
    iddfs_stats = ([], [])
    bkt_stats = ([], [])
    random_stats = ([], [])
    file = open("results.txt", "w")
    file.write("After running the 4 algorithms with 10 different sets of inputs, it seems that:\n\n")
    file.close()
    file = open("results.txt", "a")
    for instance in instances:
        file.write("For the instance: ")
        file.write(str(instance[0]) + " boat capacity, " +
                   str(instance[1]) + " missionaries and "
                   + str(instance[2]) + " cannibals, we have:\n")
        print("a_star")
        run_one_time("A*", file, instance, a_star_stats)
        print("iddfs")
        run_one_time("IDDFS", file, instance, iddfs_stats)
        print("bkt")
        run_one_time("BKT", file, instance, bkt_stats)
        bkt_flag = False
        print("random")
        run_one_time("Random", file, instance, random_stats)
        file.write('\n')

    time_a_star = sum(a_star_stats[1]) / 10
    time_iddfs = sum(iddfs_stats[1]) / 10
    time_bkt = sum(bkt_stats[1]) / 10
    time_random = sum(random_stats[1]) / 10
    length_a_star = sum(a_star_stats[0]) / 10
    length_iddfs = sum(iddfs_stats[0]) / 10
    length_bkt = sum(bkt_stats[0]) / 10
    length_random = sum(random_stats[0]) / 10

    file.write("\nMedium execution time for A*: " + str(time_a_star) + '\n')
    file.write("Medium solution length for A*: " + str(length_a_star) + '\n')
    file.write("\nMedium execution time for IDDFS: " + str(time_iddfs) + '\n')
    file.write("Medium solution length for IDDFS: " + str(length_iddfs) + '\n')
    file.write("\nMedium execution time for BKT: " + str(time_bkt) + '\n')
    file.write("Medium solution length for BKT: " + str(length_bkt) + '\n')
    file.write("\nMedium execution time for Random: " + str(time_random) + '\n')
    file.write("Medium solution length for Random: " + str(length_random) + '\n')

    file.close()


run_instances(generate_all_instances())


#print(iddfs_strategy(initialize(4, 15, 15)))
#print(bkt_strategy(initialize(4, 15, 15)))
#print(a_star(initialize(4, 9, 5)))
