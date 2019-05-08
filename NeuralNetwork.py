

import glob
import pandas as pd
import numpy as np
import math

class NeuralNet():
    def __init__(self,stateName):
        self.createMoodList(stateName)
        self.calcGausianFunction()


    def createMoodList(self,stateName):
        self.path = 'Public Mood/' + stateName + '/'
        self.moodFile = glob.glob(self.path + "*.csv")[0]
        df = pd.read_csv(self.moodFile)
        self.joy_values = df['joy']
        self.surprise_value = df['surprise']
        self.mood_list = self.joy_values+self.surprise_value
        print(self.mood_list)

    def calcGausianFunction(self, values_list):
        self.mean = np.mean(values_list)
        self.Mik_list = []
        for xi in values_list:
            self.Mik_list.append(math.exp(-((xi-self.mean)**2)/self.calcVariance(xi,self.mean)))
            print(self.Mik_list[-1])

    def calcVariance(self,xi, mean):
        return 0.5*((xi-mean)**2)


if __name__ == "__main__":
    window = NeuralNet('California')