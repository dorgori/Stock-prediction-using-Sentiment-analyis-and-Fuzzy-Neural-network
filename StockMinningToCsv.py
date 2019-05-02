import csv
import yahoofinance as yf
import datetime
from datetime import timedelta

#profile = yf.AssetProfile('AAPL')
#profile.to_csv('AAPL-profile.csv')

### share params : share symbol, start time, end time
'''
choose symbol, since date, until date
'''
symbol = 'AAPL'
since_date = '2019-01-05'
until_date = '2019-02-05'

now = datetime.datetime.now()
day = now.strftime("%A")
print(day)

if day == 'Thursday':                       #needs to be friday
    yesterday = now - timedelta(days=1)
    print(yesterday.strftime('20%y-%m-%d'))
    '''
    complete missing data from the 2 previous days
    '''
    pass
if day == 'Saturday':
    pass

share = yf.HistoricalPrices(symbol, since_date, until_date)
#share.to_csv('Stock Values/'+since_date+'.csv')
stockValue = share.to_dfs(list)



with open('Stock Values/'+since_date+'.csv') as f:
    reader = list(csv.reader(f))
    print(reader)
    f.close()

