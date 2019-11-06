class Error(Exception):
    """Base class for other exceptions"""
    pass


class WrongInputError(Error):
    """Raised when the input is not 9 lines x 9 columns containing only digits and '_' symbols"""
    pass


def read_from_file():
    matrix = [[[i for i in range(0, 10)] for j in range(9)] for k in range(9)]
    with open('matrix.txt') as fd:
        lines_from_file = fd.readlines()
    if len(lines_from_file) != 9:
        raise WrongInputError
    for line_index, line in enumerate(lines_from_file):
        line = line.strip("\n ")
        if len(line) != 9:
            raise WrongInputError
        for column_index, char in enumerate(line):
            if char not in "123456789_":
                raise WrongInputError
            if char != '_':
                matrix[line_index][column_index][0] = int(char)
    return matrix


def print_matrix(matrix):
    for line in matrix:
        for col in line:
            print(col[0], end=' ')
        print()


print_matrix(read_from_file())


def get_squares(i, j):
    all_squares = [
        [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
        [(3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2)],
        [(6, 0), (6, 1), (6, 2), (7, 0), (7, 1), (7, 2), (8, 0), (8, 1), (8, 2)],
        [(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)],
        [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)],
        [(6, 3), (6, 4), (6, 5), (7, 3), (7, 4), (7, 5), (8, 3), (8, 4), (8, 5)],
        [(0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 8), (2, 6), (2, 7), (2, 8)],
        [(3, 6), (3, 7), (3, 8), (4, 6), (4, 7), (4, 8), (5, 6), (5, 7), (5, 8)],
        [(6, 6), (6, 7), (6, 8), (7, 6), (7, 7), (7, 8), (8, 6), (8, 7), (8, 8)]
    ]
    for square in all_squares:
        if (i, j) in square:
            return square


def forward_checking(i, j, matrix):
    pass


def bkt(matrix):
    for i in range(0, 9):
        for j in range(0, 9):
            for possible_number in matrix[i][j][1:]:
                pass


print(get_squares(3, 4))
