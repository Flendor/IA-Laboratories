import numpy as np
import sys


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class Network:
    @staticmethod
    def __init_weights_between_layers(number_of_neurons_for_layer_1, number_of_neurons_for_layer_2):
        # average = 0, variance = 4
        return np.random.randn(number_of_neurons_for_layer_2, number_of_neurons_for_layer_1) * \
               np.sqrt(4 / number_of_neurons_for_layer_1)

    @staticmethod
    def __softmax(z):
        e_z = np.exp(z - np.max(z))
        return e_z / e_z.sum(axis=0)

    def __init__(self, number_of_layers, number_of_neurons_for_layer):
        self.__activation_function = sigmoid
        self.__number_of_layers = number_of_layers
        self.__number_of_neurons_for_layer = number_of_neurons_for_layer
        self.__weights = np.array([
            self.__init_weights_between_layers(number_of_neurons_for_layer[i - 1], number_of_neurons_for_layer[i]) for i
            in range(1, number_of_layers)])

    def __activation(self, z):
        return [self.__activation_function(z[i]) for i in range(len(z))]

    def train(self, inputs, outputs, iterations=10, learning_rate=0.3):
        data = list(zip(inputs, outputs))
        data_size = len(data)
        iteration_index = 0
        while iteration_index < iterations:
            np.random.shuffle(data)
            misclassified = 0

            for index, (_input, _output) in enumerate(data):
                # forward propagation
                y = [np.array(_input)]
                for layer_index in range(1, self.__number_of_layers):
                    z = self.__weights[layer_index - 1].dot(y[layer_index - 1])
                    if layer_index == self.__number_of_layers - 1:
                        y.append(np.array(self.__softmax(z)))
                    else:
                        y.append(np.array(self.__activation(z)))

                # check
                response_index = np.argmax(y[self.__number_of_layers - 1])
                if _output[response_index] != 1:
                    misclassified += 1

                # back propagation
                delta = [np.array(y[self.__number_of_layers - 1]) - np.array(_output)]
                for layer_index in range(self.__number_of_layers - 2, -1, -1):
                    delta = [np.array(np.array(y[layer_index]) *
                                      (np.array([1] * self.__number_of_neurons_for_layer[layer_index]) -
                                       np.array(y[layer_index])) *
                                      (np.array([self.__weights[layer_index].T[i].dot(delta[0]) for i in
                                                 range(len(self.__weights[layer_index].T))])))] + delta
                    for i in range(len(self.__weights[layer_index])):
                        self.__weights[layer_index][i] -= delta[1][i] * y[layer_index] * learning_rate

            iteration_index += 1
            print(f'Accuracy: {round(((data_size - misclassified) / data_size) * 100, 2)}')

    def consume(self, inputs, outputs):
        data = list(zip(inputs, outputs))
        data_size = len(data)
        misclassified = 0
        for index, (_input, _output) in enumerate(data):
            # forward propagation
            y = [np.array(_input)]
            for layer_index in range(1, self.__number_of_layers):
                z = self.__weights[layer_index - 1].dot(y[layer_index - 1])
                if layer_index == self.__number_of_layers - 1:
                    y.append(np.array(self.__softmax(z)))
                else:
                    y.append(np.array(self.__activation(z)))

            # check
            response_index = np.argmax(y[self.__number_of_layers - 1])
            if _output[response_index] != 1:
                misclassified += 1
            sys.stdout.write(f"\rThe consumption of the dataset is {round(((index + 1) / data_size) * 100, 2)}% done. ")
            sys.stdout.flush()
        print(f'Accuracy: {round((1 - (misclassified / data_size)) * 100, 2)}')

    def save(self):
        np.save("weights", self.__weights)

    def load(self):
        self.__weights = np.load("weights.npy")
