import csv, os, re
import datetime
from datetime import datetime
from datetime import date

count = 0
row = []
daily_tweet = []
start_date = ''
flag = 0

#no country

def write_to_csv(filename, tweets):
    csv_name = 'Tweets By Days/' + filename + '.csv'
    with open(csv_name, 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(['Date', 'Tweet'])
            for tweet in tweets:
                writer.writerow(tweet)

with open(start_date + ".csv", errors='ignore') as tweets_file:
    line = tweets_file.readlines()
    for val in line:
        if count ==0:
            pass
        else:
            lst = val.split(',')
            row.append(lst[0])
            lst[0] = re.sub('PDT', '', lst[0])
            lst[0] = re.sub('  ', ' ', lst[0])
            str_date = str(lst[0])

            date_time_obj = datetime.strptime(str_date, '%a %b %d %H:%M:%S %Y')
            date_time_str = date_time_obj.strftime('20%y-%m-%d')

            if flag == 0:
                start_date = date_time_str
                flag = 1
            if start_date != date_time_str:
                flag = 0
                write_to_csv(start_date, daily_tweet)
                daily_tweet = []
            lst = str(lst[1:])
            row.append(lst)
            daily_tweet.append(row)
            row = []
        count += 1

