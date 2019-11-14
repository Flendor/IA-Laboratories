from Data import *
from Network import *

network = Network(3, [7, 9, 10])

network.train(train_set_input, train_set_output, iterations=50)
network.save()

###
input("Training is done. Do you want to try it out?\nPress 'Enter' to continue.")
network = Network(3, [7, 9, 10])
network.load()
print("Training set:")
network.consume(train_set_input, train_set_output)
