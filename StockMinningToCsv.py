import csv
import yahoofinance as yf
import datetime
from datetime import timedelta
import os

#profile = yf.AssetProfile('AAPL')
#profile.to_csv('AAPL-profile.csv')
'''
need to finish grab share data for each day.
'''
### share params : share symbol, start time, end time
class StockValues:
    def __init__(self):
        self.init_symbol()
        #self.check_if_weekend()
        self.minning_share()

    '''
    choose symbol, since date, until date
    '''
    def init_symbol(self):
        self.symbol = 'AAPL'
        self.since_date = '2019-04-22'
        self.until_date = '2019-05-08'


    def minning_share(self):
        print(self.symbol)
        # share.to_csv('Stock Values/'+since_date+'.csv')
        share_data = []
        check = datetime.datetime.strptime(self.since_date, '20%y-%m-%d')
        until = datetime.datetime.strptime(self.until_date, '20%y-%m-%d')
        next_day = check + timedelta(days=1)
        while check != until:
            print(str(check.strftime('20%y-%m-%d')))
            name_day = check.strftime("%A")
            if name_day == 'Saturday' or name_day == 'Sunday':
                prev_days = []
                if len(share_data) == 0:
                    prev_days = self.complete_missing_day(2)

                elif len(share_data) == 1:
                    prev_days = self.complete_missing_day(1)
                    prev_days.append(share_data[len(share_data)-1])

                else:
                    prev_days.copy(share_data[len(share_data)-2:])

                prev_days[0].pop(0)
                prev_days[1].pop(0)
                stock_val = list(map(lambda x, y: (float(x) + float(y)) / 2, prev_days[0], prev_days[1]))
                stock_val.insert(0, check.strftime('20%y-%m-%d'))
                print(stock_val)
                share_data.append(stock_val)

            else:
                share = yf.HistoricalPrices(self.symbol, check.strftime('20%y-%m-%d'), next_day.strftime('20%y-%m-%d'))
                stock_val = share.prices.split('\n')
                stock_val = stock_val[1:-1]
                stock_val = stock_val[0].split(',')
                print(stock_val)
                share_data.append(stock_val)
               # print(share_data[len(share_data)-1])

            check = check + timedelta(days=1)
            next_day = next_day + timedelta(days=1)


        for val in share_data:
            print(val)
        self.write_into_csv(self.symbol, share_data)


    def complete_missing_day(self, file_name, num_of_days):
        '''
        1. open file
        2. read N days
        3. close file
        :return: list of values
        '''
        with open('Stock Values/' + file_name + '-prices.csv', newline='') as csvFile:
            reader = list(csv.reader(csvFile))
            if num_of_days == 1:
                reader = reader[len(reader)-1]
            elif num_of_days == 2:
                reader = reader[len(reader)-2:]
            csvFile.close()

        return reader


    def write_into_csv(self, file_name, csvData):
        flag = 0
        if not os.path.isfile(file_name) == 1:
            flag = 1
            headlines = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        with open('Stock Values/' + file_name + '-prices.csv', 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            if flag:
                writer.writerow(headlines)
            writer.writerows(csvData)
            csvFile.close()



'''
share = yf.HistoricalPrices(symbol, since_date, until_date)
#share.to_csv('Stock Values/'+since_date+'.csv')
stockValue = share.to_dfs(list)
'''



if __name__ == "__main__":
    window = StockValues()