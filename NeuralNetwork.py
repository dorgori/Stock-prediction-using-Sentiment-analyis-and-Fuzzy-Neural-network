

import glob
import pandas as pd
import numpy as np
import math, traceback
import time,csv

class NeuralNet():
    def __init__(self,stateName):
        tic = time.time()
        self.createMoodList(stateName)
        self.createStockLists()
        self.training()
        print(time.time()- tic)

    def createMoodList(self,stateName):
        self.path = 'Public Mood/' + stateName
        moodFile = glob.glob(self.path + "*.csv")[0]
        df = pd.read_csv(moodFile)
        self.joy_values = df['joy']
        self.surprise_value = df['surprise']
        self.mood_list = self.joy_values+self.surprise_value

    def calcGausianFunction(self, values_list):
        self.mean = np.mean(values_list)
        self.variance = self.calcVariance(values_list,self.mean)
        Mik_list = []
        for xi in values_list:
            expo = ((xi-self.mean)**2)/self.variance
            Mik_list.append(math.exp(-expo))
            #print(Mik_list[-1])
        return Mik_list

    def calcVariance(self,values_list, mean):
        sum = 0
        for val in values_list:
            sum += ((val-mean)**2)
        sum *= 0.5
        return sum

    def training(self):
        try:
            self.weights = np.random.rand(3)
            for i in range(0,len(self.mood_list)-2):
                #Layer 2
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
                Normalized_list = [val/mk_sum for val in self.Mk_list]
                # Layer 5
                # Calc Y total
                self.yp = [val*self.weights[i] for i,val in enumerate(Normalized_list)]
                self.y_out_total = np.sum(self.yp)

                # Calc Y desire
                """ How to calc desire output ?
                    We will use close gate of third day minus open gate of first day
                    if stock value raise by more then 1% the desired output will be 1
                    if it is less then 1 then we need to think
                """
                close_gate_ref = self.close_value[i + 2]
                open_gate_ref = self.open_values[i]
                limit_value = (open_gate_ref * 101) / 100  # This value is the raise of 1% in 3 days
                if close_gate_ref > limit_value:  # It means the stock raised by more then 1%
                    self.desired_output = 1
                else:
                    self.desired_output = close_gate_ref / limit_value
                    self.desired_output_total2 = open_gate_ref / limit_value

                # Loss function
                self.loss_function  = self.y_out_total - self.desired_output
                self.learning_rate = 0.1
                delta_w_list = [val*self.loss_function for val in Normalized_list]

                self.writeWeightToFile(self.weights)
                # Calc Back propagation
                for j in range(3):
                    new_weight = self.weights[j] - self.learning_rate * delta_w_list[j]
                    self.weights[j] = new_weight
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

    def writeWeightToFile(self,weight_list):
        with open('weight_progress.csv' ,'a',newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(weight_list)


if __name__ == "__main__":
    try:
        window = NeuralNet('California')
    except:
        print(traceback.print_exc())
