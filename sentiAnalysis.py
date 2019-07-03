import indicoio
import csv, os
import traceback
import datetime
from datetime import timedelta
import re
import pandas as pd
import config_params as cp

# single example
# orenys7_key = '0b80d9da8f4e847bd018ef74e597ad62'
# orenys8_key = '3060c861b25a9959c500910254ea1360'
# another = '74998d9369067234f28e7b23848889cd'
# ghostmaster8_key = '4d70b34b8b07b35eac0c4e16123fc3f2'
# kingdavid_key = 'a0da9e8b9fedb26fae72958acc7997ae'
# dor_key = '9870987cf69ce04962caeeddff67ce03'
# new_key = "3af4af3a50ef82c893724ab248f41e9f"
# dor_key_3 = "cc9da658f99efb5d9f27d76c5f41220a"
# ron_key = "6dcba912bcc9425a8673fcf86c811efc"
dor_key_2 = "0dce90fa65466e12c052da780741f6ee"
regex = re.compile('[^a-zA-Z ]')

class Sentiment_Analysis():
    indicoio.config.api_key = dor_key_2
    def __init__(self):
        self.emo = ['anger', 'sadness', 'fear', 'joy', 'surprise']
        today = datetime.date.today()
        yesterday = str(today - timedelta(1))
        self.initialize_start_date()
        print('Start sentiment analysis: ')
        while self.start_date != today:
            ret_val = self.classification()
            self.start_date = datetime.datetime.strptime(self.start_date, '%Y-%m-%d')
            self.start_date = self.start_date + timedelta(days=1)
            self.start_date = datetime.datetime.strftime(self.start_date, '%Y-%m-%d')
            if ret_val != -1:
                self.normalized()
                print(self.daily_p_mood.keys())
                print(self.daily_p_mood.values())
            self.saveMoodIntoCSV()

    def checkForFile(self, country):
        if not os.path.isfile("Public Mood/"+country+".csv"):
            date = '2009-05-09'
            return date
        else:
            try:
                with open("Public Mood/"+country+".csv", newline='') as mood_file:
                    reader = list(csv.reader(mood_file))
                for row in reversed(reader):
                    date = row[0]
                    break
                mood_file.close()
                date = datetime.datetime.strptime(date, '%d/%m/%Y')
                date = date + timedelta(days=1)
                date = datetime.datetime.strftime(date, '%d/%m/%Y')
                return date
            except:
                traceback.print_exc()

    def classification(self):
        try:
            with open('Csv By Days/'+ self.start_date + '.csv', newline='',encoding="ISO-8859-1") as tweetsFile:
                reader = list(csv.reader(tweetsFile))
            tweetsFile.close()
        except:
            return -1
        dailyDictionary = {'Date': '0', 'anger': 0, 'sadness': 0, 'fear': 0, 'joy': 0, 'surprise': 0}
        i=0
        # dailyDictionary['Date'] = self.start_date
        dailyDictionary['Date'] = datetime.datetime.strptime(self.start_date, '%Y-%m-%d').strftime('%m/%d/%y')
        reader.pop(0)
        marker = 0
        for row in reader:
            #if i != 10:
            if marker == 0:
                marker = 1
                continue
            try:
                row[1] = regex.sub('', row[1])
                emotions = indicoio.emotion([row[1]])
                dailyDictionary['joy'] += float(emotions[0]['joy'])
                dailyDictionary['anger'] += emotions[0]['anger']
                dailyDictionary['sadness'] += emotions[0]['sadness']
                dailyDictionary['fear'] += emotions[0]['fear']
                dailyDictionary['surprise'] += emotions[0]['surprise']
                i+=1
                if i==1000:
                  break
            except:
                traceback.print_exc()
                print(type(row[1]))
                print(i)
                continue
        #print(str(i)+ ' tweets calculated.')
        self.daily_p_mood = dailyDictionary
        return 0


    def saveMoodIntoCSV(self):
        # flag = 0
        # if not os.path.isfile('Public Mood/' + country + '.csv') == 1:
        #     flag = 1
        with open('Public Mood/' + cp.mood_file_path + '.csv', 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            # if flag == 1:
            #     writer.writerow(self.daily_p_mood.keys())
            writer.writerow(self.daily_p_mood.values())
            csvFile.close()

    def normalized(self):
        mood_sum = 0
        emotions = ['anger', 'sadness', 'fear', 'joy', 'surprise']
        for val in emotions:
            mood_sum += self.daily_p_mood[val]
        for val in emotions:
            self.daily_p_mood[val] /= mood_sum

    def initialize_start_date(self):
        df = pd.read_csv('Public Mood/' + cp.mood_file_path + '.csv')
        dates = df['Date']
        start_date = dates[len(dates) - 1]
        start_date = datetime.datetime.strptime(start_date, '%m/%d/%Y') + timedelta(days=1)
        start_date = datetime.datetime.strftime(start_date, '%Y-%m-%d')
        self.start_date = start_date

if __name__ == "__main__":
    app = Sentiment_Analysis()

