import csv
import yahoofinance as yf

#profile = yf.AssetProfile('AAPL')
#profile.to_csv('AAPL-profile.csv')

### share params : share symbol, start time, end time
share = yf.HistoricalPrices('AAPL','2019-01-01', '2019-02-02')
share.to_csv('AAPL-prices.csv')
