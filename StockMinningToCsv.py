import csv
import yahoofinance as yf
import datetime
from datetime import timedelta

#profile = yf.AssetProfile('AAPL')
#profile.to_csv('AAPL-profile.csv')
'''
need to finish grab share data for each day.
'''
### share params : share symbol, start time, end time
class StockValues:
    def __init__(self):
        self.init_symbol()
        self.check_if_weekend()

    '''
    choose symbol, since date, until date
    '''
    def init_symbol(self):
        symbol = 'AAPL'
        since_date = '2019-01-05'
        until_date = '2019-02-05'


    def read_from_csv(self, date, operation):
        with open('Stock Values/' + date + '.csv') as f:
            stock_val = list(csv.reader(f))
            print(stock_val)
            f.close()
            if operation == 'grab values':
            # remove headlines
                stock_val.remove(stock_val[0])
                stock_val = stock_val.pop()
                stock_val = stock_val[1:]
                return stock_val
            if operation == 'headlines':
                return stock_val[0]


    def minning_share(self):
        print(self.symbol)
        #share = yf.HistoricalPrices(symbol, since_date, until_date)
        # share.to_csv('Stock Values/'+since_date+'.csv')
        #stockValue = share.to_dfs(list)


    def check_if_weekend(self):
        stock_val_day1 = []
        stock_val_day2 = []
        now = datetime.datetime.now()
        day = now.strftime("%A")
        print(day)
        if day == 'Friday' or day == 'Saturday':
            yesterday = now - timedelta(days=1)
            print(yesterday.strftime('20%y-%m-%d'))
            stock_val_day1 = self.read_from_csv(yesterday, 'grab values')
            yesterday = now - timedelta(days=1)
            print(yesterday.strftime('20%y-%m-%d'))
            stock_val_day2 = self.read_from_csv(yesterday, 'grab values')
            headlines = self.read_from_csv(yesterday, 'headlines')
            stock_val = list(map(lambda x, y: (float(x)+float(y))/2, stock_val_day1, stock_val_day2))
            now.strftime('20%y-%m-%d')
            stock_val.insert(0,now)
            print (stock_val)
            self.write_into_csv(day, stock_val, headlines)
        else:
            self.minning_share()
            print(now.strftime('20%y-%m-%d'))
        return 0


    def write_into_csv(self, file_date, csvData, headlines):
        with open('Stock Values/' + file_date + '.csv', 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(headlines)
            writer.writerow(csvData)
            csvFile.close()



'''
share = yf.HistoricalPrices(symbol, since_date, until_date)
#share.to_csv('Stock Values/'+since_date+'.csv')
stockValue = share.to_dfs(list)
'''



if __name__ == "__main__":
    window = StockValues()