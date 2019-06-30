import NeuralNetwork
from Django_project.settings import PRED_URL
import numpy as np
import datetime
from datetime import timedelta
import csv
import os
import glob
import pandas as pd
import config_params as cp


class Predict():
    def __init__(self, symbol, date):
        self.path = '../'
        self.symbol = symbol
        self.date = date
        self.prev_day = datetime.datetime.strptime(self.date, '%Y-%m-%d')
        self.prev_day = self.prev_day - timedelta(days=1)
        self.prev_day = datetime.datetime.strftime(self.prev_day, '%d/%m/%Y')
        self.date = datetime.datetime.strptime(self.date, '%Y-%m-%d')
        self.date = datetime.datetime.strftime(self.date, '%d/%m/%Y')

        if self.check_if_date_existed() == 0:
            self.net = NeuralNetwork.NeuralNet(cp.PREDICT)
            self.net_predict()

        self.results = self.read_predicts()

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
        weights = self.net.readUpdateWeights(self.symbol)
        yp = [val * weights[k] for k, val in enumerate(Normalized_list)]
        y_out_total = np.sum(yp, dtype=np.float64)
        print(y_out_total)
        # write into csvFile
        if not os.path.isfile(PRED_URL + self.symbol + '-predicts.csv'):
            highlights = ['Date', 'Predict']
            with open(PRED_URL + self.symbol + '-predicts.csv', 'a+', newline='') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(highlights)
                writer.writerow([self.date, y_out_total])
        else:
            with open(PRED_URL + self.symbol + '-predicts.csv', 'a+', newline='') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow([self.date, y_out_total])

    def check_if_date_existed(self):
        if os.path.isfile(PRED_URL + self.symbol + '-predicts.csv'):
            predictFile = glob.glob(PRED_URL + self.symbol + "-predicts.csv")[0]
            df = pd.read_csv(predictFile)

            dates_list = df['Date']
            dates_list = dates_list.get_values()
            if self.prev_day in dates_list and self.date in dates_list:
                return 1
            if self.prev_day in dates_list and self.date not in dates_list:
                return 0
            if self.prev_day not in dates_list and self.date not in dates_list:
                return 1
        return 1

    def read_predicts(self):
        if os.path.isfile(PRED_URL + self.symbol + '-predicts.csv'):
            predictFile = glob.glob(PRED_URL + self.symbol + "-predicts.csv")[0]
            df = pd.read_csv(predictFile)
            predicts_list = df['Predict']
            predicts_list = predicts_list.get_values()
            predicts_list = predicts_list[-6:]
            return predicts_list
        return None

if __name__ == "__main__":
    window = Predict()
