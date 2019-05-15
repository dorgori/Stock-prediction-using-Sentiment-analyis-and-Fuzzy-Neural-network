import indicoio
import csv, os
import traceback
import datetime
from datetime import timedelta

# single example
# print(indicoio.emotion(tweet))
#orenys7_key = '0b80d9da8f4e847bd018ef74e597ad62'

class Sentiment_Analysis():
    indicoio.config.api_key = '3060c861b25a9959c500910254ea1360'
    def __init__(self):
        self.emo = ['anger', 'sadness', 'fear', 'joy', 'surprise']
        self.country = 'California'
        today = str(datetime.date.today())
        self.start_date = self.checkForFile()
        while self.start_date != today:
            self.start_date = self.checkForFile()
            self.classification(country=self.country, start_date=self.start_date)
            self.normalized()
            print(self.daily_p_mood.keys())
            print(self.daily_p_mood.values())

            self.saveMoodIntoCSV()


    def checkForFile(self):
        if not os.path.isfile("Public Mood/"+self.country+".csv"):
            date = '2019-04-22'
            return date
        else:
            try:
                with open("Public Mood/"+self.country+".csv", newline='') as mood_file:
                    reader = list(csv.reader(mood_file))
                for row in reversed(reader):
                    date = row[0]
                    break
                mood_file.close()
                date = datetime.datetime.strptime(date, '20%y-%m-%d')
                date = date + timedelta(days=1)
                date = datetime.datetime.strftime(date, '20%y-%m-%d')
                return date
            except:
                traceback.print_exc()

    def classification(self, country, start_date):
        with open('Csv By Days/' + country + '/' + start_date + '.csv', newline='') as tweetsFile:
            reader = list(csv.reader(tweetsFile))
        tweetsFile.close()
        dailyDictionary = {'Date': '0', 'anger': 0, 'sadness': 0, 'fear': 0, 'joy': 0, 'surprise': 0}
        i=0
        dailyDictionary['Date'] = self.start_date
        reader.pop(0)
        for row in reader:
            #if i != 10:
            emotions = indicoio.emotion([row[1]])
            dailyDictionary['joy'] += float(emotions[0]['joy'])
            dailyDictionary['anger'] += emotions[0]['anger']
            dailyDictionary['sadness'] += emotions[0]['sadness']
            dailyDictionary['fear'] += emotions[0]['fear']
            dailyDictionary['surprise'] += emotions[0]['surprise']
            i+=1
            #if i==11:
             #   break
        #print(str(i)+ ' tweets calculated.')
        self.daily_p_mood = dailyDictionary


    def saveMoodIntoCSV(self):
        flag = 0
        if not os.path.isfile('Public Mood/' + self.country + '.csv') == 1:
            flag = 1
        with open('Public Mood/'+self.country+'.csv', 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            if flag == 1:
                writer.writerow(self.daily_p_mood.keys())
            writer.writerow(self.daily_p_mood.values())
            csvFile.close()

    def normalized(self):
        mood_sum = 0
        emotions = ['anger', 'sadness', 'fear', 'joy', 'surprise']
        for val in emotions:
            mood_sum += self.daily_p_mood[val]
        for val in emotions:
            self.daily_p_mood[val] /= mood_sum

if __name__ == "__main__":
    app = Sentiment_Analysis()

