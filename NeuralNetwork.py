

import glob
import pandas as pd
import numpy as np
import traceback
import time,csv
import datetime, math
from datetime import timedelta
import config_params as cp
import os

class NeuralNet():
    def __init__(self, mode):
        #tic = time.time()
        self.mode = mode
        self.createMoodList()
        self.createStockLists()
        for i in range(1):
            if mode != cp.PREDICT:
                training_len = int(len(self.open_values) * 0.8)
                self.training(training_len)
                stock_name = self.StockFile.replace('Stock Values\\', "")
                stock_name = stock_name[:stock_name.find('-')].lower()
                self.testing(training_len, stock_name)
                accuracy = np.sum(self.accurate_list) / len(self.accurate_list)
                # Need to create Highlights to csv!!!!!
                with open(cp.accuracy_file + stock_name + '.csv', 'a+', newline='') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow([self.weights[0], self.weights[1], self.weights[2],accuracy])
                print(accuracy)
        #print(time.time()- tic)

    def createMoodList(self):
        self.path = 'Public Mood/' + cp.mood_file_path
        if self.mode == cp.PREDICT:
            self.path = '../Public Mood/' + cp.mood_file_path
        moodFile = glob.glob(self.path + ".csv")[0]
        df = pd.read_csv(moodFile)
        self.joy_values = df['joy']
        self.surprise_value = df['surprise']
        #self.mood_list = self.joy_values + self.surprise_value
        self.mood_list = self.joy_values
        self.date_list = df['Date']

    def calcGausianFunction(self, values_list):
        mean = np.mean(values_list)
        std = np.std(values_list)
        if std == 0:
            std = 0.00512
        Mik_list = self.gaussmf(values_list, mean, std)
        return Mik_list

    def training(self, end_index):
        try:
            self.weights = abs(np.random.rand(3))

            for i in range(0, end_index - 2):
                # TODO: Layer 2
                if self.validDateContiously(i) == -1:  # Date jump
                    #print('Date jump ' + str(self.date_list[i]))
                    continue

                Mik_mood_list = self.calcGausianFunction(self.mood_list[i:i + 3])
                Mik_open_list = self.calcGausianFunction(self.open_values[i:i + 3])
                Mik_close_list = self.calcGausianFunction(self.close_value[i:i + 3])
                Mik_high_list = self.calcGausianFunction(self.high_value[i:i + 3])
                Mik_low_list = self.calcGausianFunction(self.low_value[i:i + 3])
                Mik_total = [Mik_mood_list, Mik_open_list, Mik_close_list, Mik_high_list, Mik_low_list]
                # TODO: Layer 3
                Mk_list = self.createMkList(Mik_total)

                # TODO: Layer 4
                mk_sum = np.sum(Mk_list)
                Normalized_list = [val / mk_sum for val in Mk_list]

                # TODO: Layer 5 Y total
                yp = [val * self.weights[k] for k, val in enumerate(Normalized_list)]
                y_out_total = np.sum(yp, dtype=np.float64)

                # TODO: Calc Y desire
                close_gate_ref = self.close_value[i + 2]
                open_gate_ref = self.open_values[i]
                self.setDesiredValue(open_gate_ref, close_gate_ref)

                # TODO: Loss function
                loss_function = math.pow(y_out_total - self.desired_output, 2)
                learning_rate = 0.01
                delta_w_list = [val * loss_function for val in Normalized_list]

                #TODO: Calc Back propagation
                for j in range(cp.Num_Weights):
                    new_weight = self.weights[j] - learning_rate * delta_w_list[j]
                    self.weights[j] = new_weight

        except:
            print(traceback.print_exc())

    def createStockLists(self):
        self.path = 'Stock Values/'
        if self.mode == cp.PREDICT:
            self.path = '../Stock Values/'
        self.StockFile = glob.glob(self.path+"*.csv")[0]
        print(self.StockFile)
        df = pd.read_csv(self.StockFile)
        self.open_values = df['Open']
        self.close_value = df['Close']
        self.high_value = df['High']
        self.low_value = df['Low']

    def createMkList(self, Mik_total):
        Mk_list = []
        multiply = 1
        for i in range(cp.Num_Weights):
            for val in Mik_total:
                multiply *= val[i]
            Mk_list.append(multiply)
            multiply = 1
        return  Mk_list

    """ How to calc desire output ?
                                We will use close gate of third day minus open gate of first day
                                if stock value raise by more then 1% the desired output will be 1
                                if it is less then 1 then we need to think
                            """
    def setDesiredValue(self,open_value, close_value):
        upper_limit_value = (open_value * 102) / 100    # This value present raise of 2% in 3 days
        upper_limit_value_1_5 = (open_value * 101.5) / 100  # This value present raise of 1.5% in 3 days
        upper_limit_value_1 = (open_value * 101) / 100  # This value present raise of 1% in 3 days
        buy_high_limit = (open_value * 100.8) / 100     # This value present raise of 0.8% in 3 days
        buy_meidum_limit = (open_value * 100.6) / 100   # This value present raise of 0.6% in 3 days

        stay_lower_limit = (open_value * 99.6) / 100    # This value present decline of 0.4% in 3 days
        sell_upper_limit = (open_value * 99.4) / 100    # This value present decline of 0.6% in 3 days
        sell_lower_limit = (open_value * 99.2) / 100    # This value present decline of 0.8% in 3 days

        if close_value > upper_limit_value:
            self.desired_output = 1
        if close_value > upper_limit_value_1_5:
            self.desired_output = 0.9
        if close_value > upper_limit_value_1:
            self.desired_output = 0.85
        elif close_value > buy_high_limit:
            self.desired_output = 0.8
        elif close_value > buy_meidum_limit:
            self.desired_output = 0.7
        elif close_value >=stay_lower_limit:
            self.desired_output = 0.5
        elif close_value > sell_upper_limit:
            self.desired_output = 0.3
        elif close_value > sell_lower_limit:
            self.desired_output = 0.1
        else:
            self.desired_output = 0.0

    def validDateContiously(self,start_index):
        try:
            first_day = datetime.datetime.strptime(self.date_list[start_index], '%m/%d/%Y')
            second_day = datetime.datetime.strptime(self.date_list[start_index + 1], '%m/%d/%Y')
            third_day = datetime.datetime.strptime(self.date_list[start_index + 2], '%m/%d/%Y')
            if first_day != second_day - timedelta(days=1) or first_day != third_day - timedelta(days=2):
                return -1
            return 0
        except:
            traceback.print_exc()

    def testing(self, start_index, symbol):
        self.accurate_list = []
        weights = self.readUpdateWeights(symbol)
        #weights = self.weights

        try:
            for i in range(start_index, len(self.open_values) - 2):
                #Layer 2
                if self.validDateContiously(i) == -1:  # Date jump
                    continue
                Mik_mood_list = self.calcGausianFunction(self.mood_list[i - 3:i])
                Mik_open_list = self.calcGausianFunction(self.open_values[i - 3:i])
                Mik_close_list = self.calcGausianFunction(self.close_value[i - 3:i])
                Mik_high_list = self.calcGausianFunction(self.high_value[i - 3:i])
                Mik_low_list = self.calcGausianFunction(self.low_value[i - 3:i])

                Mik_total = [Mik_mood_list, Mik_open_list, Mik_close_list, Mik_high_list, Mik_low_list]
                # TODO: Layer 3
                Mk_list = self.createMkList(Mik_total)

                # TODO: Layer 4
                mk_sum = np.sum(Mk_list)
                Normalized_list = [val / mk_sum for val in Mk_list]
                # Layer 5
                # TODO: Calc Y total
                yp = [val * weights[k] for k,val in enumerate(Normalized_list)]
                y_out_total = (np.sum(yp))
                print(i)
                print(y_out_total)
                # TODO: Calc Y desire
                close_gate_ref_today = self.close_value[i]
                open_gate_ref_today = self.open_values[i]
                self.checkAccuracy(open_gate_ref_today, close_gate_ref_today , y_out_total)
        except:
            print(traceback.print_exc())

    def checkAccuracy(self, open_val, close_val, y_out):
        if close_val - open_val > 0:  # Stock was raised
            if y_out >= 0.7:
                self.accurate_list.append(1)
            elif y_out <= 0.3:
                self.accurate_list.append(0)
            else:
                self.accurate_list.append(0.5)
        elif close_val - open_val < 0:  # Stock was decreased
            if y_out >= 0.7:
                self.accurate_list.append(0)
            elif y_out <= 0.3:
                self.accurate_list.append(1)
            else:
                self.accurate_list.append(0.5)

    def readUpdateWeights(self, symbol):
        if self.mode == cp.PREDICT:
            self.path = '../' + cp.train_weights_file
            df = pd.read_csv(self.path + symbol + '.csv')
        else:
            df = pd.read_csv(cp.train_weights_file + symbol + '.csv')
        w1 = df['w1'][-1:]
        w2 = df['w1'][-1:]
        w3 = df['w3'][-1:]
        weights = [w1, w2, w3]
        return weights

    def gaussmf(self, x, c, v):
        """Compute Gaussian Membership function. """
        y = [np.exp(-np.power((i - c), 2) / (2 * v ** 2.0)) for i in x]
        return y

if __name__ == "__main__":
    try:
        window = NeuralNet(cp.Training)
    except:
        print(traceback.print_exc())
