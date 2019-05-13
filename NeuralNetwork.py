

import glob
import pandas as pd
import numpy as np
import math

class NeuralNet():
    def __init__(self,stateName):
        self.createMoodList(stateName)
        self.createStockLists()
        self.training()
        #self.calcGausianFunction()


    def createMoodList(self,stateName):
        self.path = 'Public Mood/' + stateName + '/'
        moodFile = glob.glob(self.path + "*.csv")[0]
        df = pd.read_csv(moodFile)
        self.joy_values = df['joy']
        self.surprise_value = df['surprise']
        self.mood_list = self.joy_values+self.surprise_value
        #print(self.mood_list)

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
        self.weights = np.random.rand(3)
        for i in range(0,round(len(self.mood_list)-2)):
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
            Normalized_list = []
            for val in self.Mk_list:
                Normalized_list.append(val / np.sum(self.Mk_list))

            # Layer 5
            y_out = 0
            for j, val in enumerate(Normalized_list):
                y_out += val*self.weights[j]
            print(y_out)
            """ How to calc desire output ?
                We will use close gate of third day minus open gate of first day
                if stock value raise by more then 1% the desired output will be 1
                if it is less then 1 then we need to think
            """
            close_gate_ref = self.close_value[i+2]
            open_gate_ref = self.open_values[i]
            #diff_ref = close_gate_ref - open_gate_ref
            limit_value = (open_gate_ref*101) / 100     # This is the 1% limit
            stock_change = close_gate_ref / limit_value
            if close_gate_ref > limit_value:            # It means the stock raised by more then 1%
                self.desired_output = 1
            else:
                self.desired_output = close_gate_ref / limit_value
                self.desired_output2 = open_gate_ref / limit_value
            print(close_gate_ref)

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


if __name__ == "__main__":
    window = NeuralNet('California')
