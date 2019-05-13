import indicoio
import csv, os
import traceback
import datetime
from datetime import timedelta

# single example
# print(indicoio.emotion(tweet))

class Sentiment_Analysis():
    indicoio.config.api_key = '0b80d9da8f4e847bd018ef74e597ad62'
    def __init__(self):
        self.emo = ['anger', 'sadness', 'fear', 'joy', 'surprise']
        self.country = 'California'
        self.start_date = self.checkForFile()
        print("stage1: date")
        self.classification(country=self.country, start_date=self.start_date)
        print("stage2.2: classification")
        print(self.daily_p_mood.keys())
        print(self.daily_p_mood.values())
        self.saveMoodIntoCSV()
        self.main()


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
                date = datetime.datetime.strptime(date, '20%y-%m-%8d')
                date = date + timedelta(days=1)
                date = datetime.datetime.strftime(date, '20%y-%m-%d')
                return date
            except:
                traceback.print_exc()

    def classification(self, country, start_date):
        with open('Csv By Days/' + country + '/' + start_date + '.csv', newline='') as tweetsFile:
            reader = list(csv.reader(tweetsFile))
        tweetsFile.close()
        print("stage2: after reading")
        emotions_classification = []
        p_mood = []
        dailyDictionary = {'Date': '0', 'anger': 0, 'sadness': 0, 'fear': 0, 'joy': 0, 'surprise': 0}
        i=0
        dailyDictionary['Date'] = self.start_date
        reader.pop(0)
        for row in reader:
            if i != 10:
                emotions = indicoio.emotion([row[1]])
                dailyDictionary['joy'] += float(emotions[0]['joy'])
                dailyDictionary['anger'] += emotions[0]['anger']
                dailyDictionary['sadness'] += emotions[0]['sadness']
                dailyDictionary['fear'] += emotions[0]['fear']
                dailyDictionary['surprise'] += emotions[0]['surprise']
            i+=1
            print("stage2.3: " + str(i))
            if i==11:
                break
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
    def main(self):
            '''
            Choose which country we want to calculate from the GUI
            country = selectedItem
            choose which date we want to calculate
            date = selectedDate

           # country = 'California'
           # first_date = '2019-04-22'
           # self.checkForFile(country)

          emotions = self.classification()
            i = 0
            cnt = 0
            dailyDictionary = {'anger': 0, 'sadness': 0, 'fear': 0, 'joy': 0, 'surprise': 0}

            #summarize the public mood
            for val in emotions:
                cnt+=1
                dailyDictionary['joy'] += val['joy']
                dailyDictionary['anger'] += val['anger']
                dailyDictionary['sadness'] += val['sadness']
                dailyDictionary['fear'] += val['fear']
                dailyDictionary['surprise'] += val['surprise']

            print(dailyDictionary) #dictionary before normalize
            print(cnt)
            key_max = max(dailyDictionary.keys(), key=(lambda k: dailyDictionary[k]))
            ###max_value = dailyDictionary[key_max]
            dict_sum = sum(dailyDictionary.values())
            normalizelist = list(map(lambda v: v/dict_sum, dailyDictionary.values()))

            for i, val in enumerate(self.emo):
                dailyDictionary[val] = normalizelist[i]

            self.saveMoodIntoCSV(country, first_date, dailyDictionary)
            print(dailyDictionary)  #dictionary after normalize
            '''
            print("HI")



if __name__ == "__main__":
    app = Sentiment_Analysis()

