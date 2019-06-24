

import NeuralNetwork
import config_params as cp
import numpy as np

class Predict():
    def __init__(self):
        self.net = NeuralNetwork.NeuralNet(cp.PREDICT)
        self.net_predict()

    def net_predict(self):
        # TODO: Layer 2
        Mik_mood_list = self.net.calcGausianFunction(self.net.mood_list[-3:])
        Mik_open_list = self.net.calcGausianFunction(self.net.open_values[-3:])
        Mik_close_list = self.net.calcGausianFunction(self.net.close_value[-3:])
        Mik_high_list = self.net.calcGausianFunction(self.net.high_value[-3:])
        Mik_low_list = self.net.calcGausianFunction(self.net.low_value[-3:])

        Mik_total = [Mik_mood_list, Mik_open_list, Mik_close_list, Mik_high_list, Mik_low_list]

        # TODO: Layer 3
        Mk_list = []
        for i in range(len(Mik_mood_list)):
            multiply = 1
            for val in Mik_total:
                multiply *= val[i]
            Mk_list.append(multiply)
            multiply = 1

        # TODO:  Layer 4
        mk_sum = np.sum(Mk_list)
        Normalized_list = [val / mk_sum for val in Mk_list]

        # TODO:  Layer 5 - Predict
        weights = self.net.readUpdateWeights()
        yp = [val * weights[k] for k, val in enumerate(Normalized_list)]
        y_out_total = np.sum(yp, dtype=np.float64)
        print(y_out_total)


if __name__ == "__main__":
    window = Predict()
