import numpy as np

with open("segments.data", "r") as data_file:
    line = data_file.readline().split()
    input_size = int(line[0])
    output_size = int(line[1])
    data_size = int(line[2])
    train_set_input = []
    train_set_output = []
    for row_index in range(data_size):
        line = data_file.readline().split(',')
        train_set_input += [[int(c) for c in line[:7]]]
        train_set_output += [[int(c) for c in line[7:]]]

    train_set_input = np.array(train_set_input)
    train_set_output = np.array(train_set_output)
