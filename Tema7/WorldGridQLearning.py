import numpy as np
import sys


def get_actions():
    return ["up", "down", "left", "right"]


def init_cell():
    return {
        "up": 0.00,
        "down": 0.00,
        "left": 0.00,
        "right": 0.00,
        "reward": -0.04
    }


def init_matrix(matrix_size):
    matrix = []
    for i in range(matrix_size):
        matrix += [[init_cell() for i in range(matrix_size)]]
    return matrix


def init_goal(matrix, stop):
    matrix[stop[0]][stop[1]]['reward'] = 1
    matrix[stop[0]][stop[1]]['up'] = 0
    matrix[stop[0]][stop[1]]['down'] = 0
    matrix[stop[0]][stop[1]]['left'] = 0
    matrix[stop[0]][stop[1]]['right'] = 0
    return matrix


def draw_matrix(matrix, walls, stop):
    print()
    for (i, row) in enumerate(matrix):
        for (j, cell) in enumerate(row):
            if (i, j) in walls:
                print("BBBBBBBBBBBBBBB", end=" @ ")
            elif (i, j) == stop:
                print("     +1.00     ", end=" @ ")
            else:
                if cell['up'] >= 0.0:
                    print("     +%.2f     " % cell['up'], end=" @ ")
                else:
                    print("     %.2f     " % cell['up'], end=" @ ")
        print()
        for (j, cell) in enumerate(row):
            if (i, j) in walls:
                print("BBBBBBBBBBBBBBB", end=" @ ")
            elif (i, j) == stop:
                print("+1.00     +1.00", end=" @ ")
            else:
                if cell['left'] >= 0.0:
                    print("+%.2f" % cell['left'], end="")
                else:
                    print("%.2f" % cell['left'], end="")
                print("     ", end="")
                if cell['right'] >= 0.0:
                    print("+%.2f" % cell['right'], end=" @ ")
                else:
                    print("%.2f" % cell['right'], end=" @ ")
        print()
        for (j, cell) in enumerate(row):
            if (i, j) in walls:
                print("BBBBBBBBBBBBBBB", end=" @ ")
            elif (i, j) == stop:
                print("     +1.00     ", end=" @ ")
            else:
                if cell['down'] >= 0.0:
                    print("     +%.2f     " % cell['down'], end=" @ ")
                else:
                    print("     %.2f     " % cell['down'], end=" @ ")
        print()
        for (j, cell) in enumerate(row):
            print(f"@@@@@@@@@@@@@@@", end=" @ ")
        print()


def get_next_position(current_position, chosen_action, n, walls):
    next_position = current_position
    if chosen_action == "up":
        next_position = (current_position[0] - 1, current_position[1] + 0)
    if chosen_action == "down":
        next_position = (current_position[0] + 1, current_position[1] + 0)
    if chosen_action == "left":
        next_position = (current_position[0] + 0, current_position[1] - 1)
    if chosen_action == "right":
        next_position = (current_position[0] + 0, current_position[1] + 1)
    if next_position[0] < 0 or next_position[0] >= n \
            or next_position[1] < 0 or next_position[1] >= n \
            or next_position in walls:
        return current_position
    return next_position


def get_max_q(matrix, current_position):
    max_val = 0
    max_action = ""
    for action in get_actions():
        if matrix[current_position[0]][current_position[1]][action] > max_val:
            max_val = matrix[current_position[0]][current_position[1]][action]
            max_action = action
    return max_val, max_action


def get_min_q(matrix, current_position):
    min_val = 1
    min_action = ""
    for action in get_actions():
        if matrix[current_position[0]][current_position[1]][action] < min_val:
            min_val = matrix[current_position[0]][current_position[1]][action]
            min_action = action
    return min_val, min_action


def q_learning(matrix, n, walls, start, stop, iterations=10, alpha=.5, gamma=1, epsilon=.7):
    # probabilities of taking the best action (1st) vs the other ones (2nd, 3rd, 4th)
    probs = [1 - epsilon, epsilon / 3, epsilon / 3, epsilon / 3]

    for iteration in range(iterations):
        current_position = start
        while current_position != stop:
            # search the best action to take
            min_current_val, min_current_action = get_min_q(matrix, current_position)

            # take that action with a probability of 1-epsilon
            actions = get_actions()
            actions.remove(min_current_action)
            actions = [min_current_action] + actions
            chosen_action = np.random.choice(actions, p=probs)

            # get the next position based on the chosen action
            next_position = get_next_position(current_position, chosen_action, n, walls)

            # save the maximum Q value of the next position
            max_next_val, max_next_action = get_max_q(matrix, next_position)

            # black magic
            matrix[current_position[0]][current_position[1]][chosen_action] += \
                alpha * (matrix[next_position[0]][next_position[1]]['reward'] +
                         gamma * max_next_val -
                         matrix[current_position[0]][current_position[1]][chosen_action])

            # take the step
            current_position = next_position

        sys.stdout.write(f"\rQ-Learning is  {round(((iteration + 1) / iterations) * 100, 2)}% done. ")


def walk(matrix, n, walls, start, stop):
    current_position = start
    saved_walk = [current_position]
    while current_position != stop:
        max_current_val, max_current_action = get_max_q(matrix, current_position)

        next_position = get_next_position(current_position, max_current_action, n, walls)

        saved_walk += [next_position]

        if current_position == next_position:
            break
        current_position = next_position
    return saved_walk


# setup
start = (0, 0)
stop = (5, 5)
n = 6
matrix = init_matrix(n)
matrix = init_goal(matrix, stop)

walls = {(1, 0), (3, 0), (4, 1), (5, 2), (3, 3),
         (4, 4), (1, 2), (1, 3), (1, 4)}

# Q-Learning
q_learning(matrix=matrix, n=n, start=start, walls=walls, stop=stop, iterations=1000)
# Display policy
draw_matrix(matrix, walls, stop)

# Read the best walk
saved_walk = walk(matrix=matrix, n=n, start=start, walls=walls, stop=stop)
if saved_walk[-1] == stop:
    print("I did it!")
else:
    print(f"I couldn't get to {stop}!")

print("The best walk I found is:")
print(saved_walk)
print(f"It has a lenght of: {len(saved_walk)}")
