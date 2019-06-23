

import glob
import pandas as pd
import numpy as np
import math, traceback
import time,csv
import datetime, math
from datetime import timedelta
import config_params as cp

training_start_index = 0
Num_Weights = 3
mood_file_path = 'good_analysis_mood'

class NeuralNet():
    def __init__(self, mode):
        #tic = time.time()
        self.createMoodList()
        self.createStockLists()
        if mode != cp.PREDICT:
            self.training(len(self.mood_list) - 20)
            self.testing(len(self.mood_list) - 20)
            acuracy = np.sum(self.accurate_list) / len(self.accurate_list)
            with open('test_accu.csv', 'a+', newline='') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(self.accurate_list)

        print(acuracy)
        #print(time.time()- tic)

    def createMoodList(self):
        self.path = 'Public Mood/' + mood_file_path
        moodFile = glob.glob(self.path + "*.csv")[0]
        df = pd.read_csv(moodFile)
        self.joy_values = df['joy']
        self.surprise_value = df['surprise']
        # self.mood_list = self.joy_values+self.surprise_value
        self.mood_list = self.joy_values
        self.date_list = df['Date']

    def calcGausianFunction(self, values_list):
        self.mean = np.mean(values_list)
        self.variance = self.calcVariance(values_list,self.mean)
        Mik_list = []
        for xi in values_list:
            expo = ((xi-self.mean)**2)/self.variance
            Mik_list.append(math.exp(-expo))
        return Mik_list

    def calcVariance(self,values_list, mean):
        sum = 0
        for val in values_list:
            sum += ((val-mean)**2)
        #sum *= 0.5
        #sum = np.var(values_list)
        return sum

    def training(self, end_index):
        try:
            self.weights = np.random.rand(3)
            #self.weights = [0.03,0.03,0.05]
            print(self.weights)
            for i in range(0, 98):
                #Layer 2
                if self.validDateContiously(i) == -1:  # Date jump
                    #print('Date jump ' + str(self.date_list[i]))
                    continue
                # print(str(self.date_list[i]))
                self.Mik_mood_list = self.calcGausianFunction(self.mood_list[i:i + 3])
                self.Mik_open_list = self.calcGausianFunction(self.open_values[i:i + 3])
                self.Mik_close_list = self.calcGausianFunction(self.close_value[i:i + 3])
                self.Mik_high_list = self.calcGausianFunction(self.high_value[i:i + 3])
                self.Mik_low_list = self.calcGausianFunction(self.low_value[i:i + 3])

                self.Mik_total = [self.Mik_mood_list,self.Mik_open_list,self.Mik_close_list,
                                  self.Mik_high_list, self.Mik_low_list]
                #Layer 3
                self.Mk_list = self.createMkList()

                #Layer 4
                mk_sum = np.sum(self.Mk_list)
                Normalized_list = [val / mk_sum for val in self.Mk_list]
                # Layer 5
                # Calc Y total
                self.yp = [val * self.weights[k] for k, val in enumerate(Normalized_list)]
                self.y_out_total = np.sum(self.yp,dtype=np.float64)

                # Calc Y desire
                close_gate_ref = self.close_value[i + 2]
                open_gate_ref = self.open_values[i]
                self.setDesiredValue(open_gate_ref, close_gate_ref)

                # Loss function
                # print(self.y_out_total)
                self.y_out_total = float(self.y_out_total)

                print(i)
                print('Y-out')
                print(self.y_out_total)
                print('Y-desire')
                print(self.desired_output)
                self.loss_function  = math.pow(self.y_out_total - self.desired_output, 2)
                self.learning_rate = 0.05
                delta_w_list = [val*self.loss_function for val in Normalized_list]

                #print(str(i) + ' ' + str(open_gate_ref))
                self.writeWeightToFile(self.weights, self.loss_function, i)

                # Calc Back propagation
                for j in range(Num_Weights):
                    new_weight = self.weights[j] - self.learning_rate * delta_w_list[j]
                    self.weights[j] = new_weight
            # print(self.weights)
            print(self.date_list[i])
            print('weights')
            print(self.weights)

        except:
            print(traceback.print_exc())

    def createStockLists(self):
        self.path = 'Stock Values/'
        StockFile = glob.glob(self.path+"*.csv")[0]
        df = pd.read_csv(StockFile)
        self.open_values = df['Open']
        self.close_value = df['Close']
        self.high_value = df['High']
        self.low_value = df['Low']

    def createMkList(self):
        Mk_list = []
        multiply = 1
        for i in range(len(self.Mik_mood_list)):
            for val in self.Mik_total:
                multiply *= val[i]
            Mk_list.append(multiply)
            multiply = 1
        return  Mk_list

    def writeWeightToFile(self, weight_list, loss, index):
        curr_time = time.strftime("%H_%M_%S")
        self.weight_file_name = 'weights_' + curr_time + '.csv'
        to_write = list(weight_list)
        to_write.append(loss)
        with open(self.weight_file_name, 'a+', newline='') as csvFile:
            writer = csv.writer(csvFile)
            if index == 0 : ## this weights is the random chosen weights
                writer.writerow(['W1', 'W2', 'W3','Loss'])
            writer.writerow(to_write)
            #print('loss '+str(loss))

    """ How to calc desire output ?
                                We will use close gate of third day minus open gate of first day
                                if stock value raise by more then 1% the desired output will be 1
                                if it is less then 1 then we need to think
                            """
    def setDesiredValue(self,open_value, close_value):

        upper_limit_value = (open_value * 101) / 100    # This value present raise of 1% in 3 days
        buy_high_limit = (open_value * 100.8) / 100     # This value present raise of 0.8% in 3 days
        buy_meidum_limit = (open_value * 100.6) / 100   # This value present raise of 0.6% in 3 days
        buy_low_limit = (open_value * 100.4) / 100      # This value present raise of 0.4% in 3 days
        stay_upper_limit = (open_value * 100.2) / 100   # This value present raise of 0.2% in 3 days
        equal = open_value                              # This value present no change
        stay_medium_limit = (open_value * 99.8) / 100   # This value present decline of 0.2% in 3 days
        stay_lower_limit = (open_value * 99.6) / 100    # This value present decline of 0.4% in 3 days
        sell_upper_limit = (open_value * 99.4) / 100    # This value present decline of 0.6% in 3 days
        sell_lower_limit = (open_value * 99.2) / 100    # This value present decline of 0.8% in 3 days
        lower_limit_value = (open_value * 99) / 100     # This value present decline of 1% in 3 days
        if close_value > upper_limit_value:
            self.desired_output = 1
        # else:
        #     self.desired_output = 0
        # return
        elif close_value > buy_high_limit:
            self.desired_output = 0.9
        elif close_value > buy_meidum_limit:
            self.desired_output = 0.8
        elif close_value > buy_low_limit:
            self.desired_output = 0.7
        elif close_value > stay_upper_limit:
            self.desired_output = 0.6
        elif close_value > equal:
            self.desired_output = 0.5
        elif close_value > stay_medium_limit:
            self.desired_output = 0.4
        elif close_value > stay_lower_limit:
            self.desired_output = 0.3
        elif close_value > sell_upper_limit:
            self.desired_output = 0.2
        elif close_value > sell_lower_limit:
            self.desired_output = 0.1
        elif close_value > lower_limit_value:
            self.desired_output = 0
        else:
            self.desired_output = 0
        return self.desired_output

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

    def testing(self, start_index):
        #self.weights = np.random.rand(3)
        #print('weights')
        #print(self.weights)
        #print(self.date_list[start_index])
        self.accurate_list = []
        try:
            for i in range(98, len(self.mood_list) - 2):
                print(i)
                #Layer 2
                if self.validDateContiously(i) == -1:  # Date jump
                    print('Date jump ' + str(self.date_list[i]))
                    continue
                # print(str(self.date_list[i]))
                self.Mik_mood_list = self.calcGausianFunction(self.mood_list[i - 3:i])
                self.Mik_open_list = self.calcGausianFunction(self.open_values[i - 3:i])
                self.Mik_close_list = self.calcGausianFunction(self.close_value[i - 3:i])
                self.Mik_high_list = self.calcGausianFunction(self.high_value[i - 3:i])
                self.Mik_low_list = self.calcGausianFunction(self.low_value[i - 3:i])

                self.Mik_total = [self.Mik_mood_list,self.Mik_open_list,self.Mik_close_list,
                                  self.Mik_high_list, self.Mik_low_list]
                #Layer 3
                self.Mk_list = self.createMkList()

                #Layer 4
                mk_sum = np.sum(self.Mk_list)
                Normalized_list = [val/mk_sum for val in self.Mk_list]
                # Layer 5
                # Calc Y total
                self.yp = [val*self.weights[k] for k,val in enumerate(Normalized_list)]
                y_out_total = np.sum(self.yp)
                y_out_total = abs(y_out_total)
                print(y_out_total)
                # Calc Y desire
                # close_gate_ref = self.close_value[i - 1]
                # open_gate_ref = self.open_values[i - 3]
                # recommendation = self.setDesiredValue(open_gate_ref, close_gate_ref)
                close_gate_ref_today = self.close_value[i]
                open_gate_ref_today = self.open_values[i]
                if close_gate_ref_today - open_gate_ref_today > 0: # Stock was raised
                    if y_out_total >= 0.7:
                        self.accurate_list.append(1)
                    elif self.y_out_total <= 0.3:
                        self.accurate_list.append(0)
                    else:
                        self.accurate_list.append(0.5)
                elif close_gate_ref_today - open_gate_ref_today < 0: # Stock was decreased
                    if y_out_total >= 0.7:
                        self.accurate_list.append(0)
                    elif self.y_out_total <= 0.3:
                        self.accurate_list.append(1)
                    else:
                        self.accurate_list.append(0.5)



        except:
            print(traceback.print_exc())

if __name__ == "__main__":
    try:
        window = NeuralNet(cp.Training)
    except:
        print(traceback.print_exc())
