import csv
import yahoofinance as yf
import datetime
from datetime import timedelta
import os
import copy

class StockValues:
    def __init__(self):
        self.file_name = '-prices.csv'
        symbol_list = ['SCCO', 'NDAQ', 'SNP', 'AAPL', 'AMZN']
        for symb in symbol_list:
            self.init_symbol(symb)
            self.minning_share()

    '''
    choose symbol, since date, until date
    '''
    def init_symbol(self, symbol):
        self.symbol = symbol
        self.since_date = '2019-06-27'
        self.until_date = '2019-06-30'

    def minning_share(self):
        share_data = []
        check = datetime.datetime.strptime(self.since_date, '20%y-%m-%d')
        until = datetime.datetime.strptime(self.until_date, '20%y-%m-%d')
        next_day = check + timedelta(days=1)
        while check != until:
            name_day = check.strftime("%A")
            if name_day == 'Saturday' or name_day == 'Sunday':
                prev_days = []
                if len(share_data) == 0:
                    prev_days = self.complete_missing_day(2)

                elif len(share_data) == 1:
                    prev_days = self.complete_missing_day(1)
                    prev_days.append(copy.deepcopy(share_data[len(share_data)-1]))

                else:
                    prev_days = copy.deepcopy(share_data[len(share_data)-2:])

                prev_days[0].pop(0)
                prev_days[1].pop(0)
                stock_val = list(map(lambda x, y: (float(x) + float(y)) / 2, prev_days[0], prev_days[1]))
                stock_val.insert(0, check.strftime('20%y-%m-%d'))
                share_data.append(stock_val)

            else:
                share = yf.HistoricalPrices(self.symbol, check.strftime('20%y-%m-%d'), next_day.strftime('20%y-%m-%d'))
                stock_val = share.prices.split('\n')
                stock_val = stock_val[1:-1]
                stock_val = stock_val[0].split(',')
                share_data.append(stock_val)

            check = check + timedelta(days=1)
            next_day = next_day + timedelta(days=1)

        # self.write_into_csv(self.symbol, share_data)
            self.write_into_csv([stock_val])


    def complete_missing_day(self, num_of_days):
        '''
        1. open file
        2. read N days
        3. close file
        :return: list of values
        '''
        with open('Stock Values/' + self.symbol + self.file_name, newline='') as csvFile:
            reader = list(csv.reader(csvFile))
            if num_of_days == 1:
                reader = reader[len(reader)-1]
            elif num_of_days == 2:
                reader = reader[len(reader)-2:]
            csvFile.close()
        return reader

    def write_into_csv(self, csvData):
        flag = 0
        if not os.path.isfile('Stock Values/' + self.symbol +  self.file_name) == 1:
            flag = 1
            headlines = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        with open('Stock Values/' + self.symbol + self.file_name, 'a+', newline='') as csvFile:
            writer = csv.writer(csvFile)
            if flag == 1:
                writer.writerow(headlines)
            writer.writerows(csvData)
            csvFile.close()

if __name__ == "__main__":
    window = StockValues()