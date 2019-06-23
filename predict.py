

import NeuralNetwork
import config_params as cp

class predict():
    def __init__(self):
        self.net = NeuralNetwork.NeuralNet(cp.PREDICT)