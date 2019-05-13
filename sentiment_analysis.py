import indicoio
import csv, os
import traceback
indicoio.config.api_key = '0b80d9da8f4e847bd018ef74e597ad62'

# single example
# print(indicoio.emotion(tweet))

class Sentiment_Analysis():

    def __init__(self):
        self.emo = ['anger', 'sadness', 'fear', 'joy', 'surprise']
        self.main()

    def classification(self, file_name):

        with open(file_name, newline='') as tweetsFile:
            reader = list(csv.reader(tweetsFile))
        tweetsFile.close()

        emotions_classification = []
        i=0
        for row in reader:
            if i!=15:
                emotions_classification.append(indicoio.emotion(row[1]))
            i+=1
            if i==16:
                return emotions_classification
        return emotions_classification



    def saveMoodIntoCSV(self, country, date, dailyDictionary):
        with open("Public Mood/"+country+"/"+date+".csv", 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            i=0
            writer.writerow(self.emo)
            values = []
            for i in range(len(self.emo)):
                values.append(dailyDictionary[self.emo[i]])
            writer.writerow(values)

    def main(self):
            '''
            Choose which country we want to calculate from the GUI
            country = selectedItem
            choose which date we want to calculate
            date = selectedDate
            '''
            country = 'California'
            first_date = '2019-04-22'
            self.checkForFile(country)
            emotions = self.classification("Csv By Days/"+country+".csv")
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

    def checkForFile(self, country):
        if not os.path.isfile("Public Mood/"+country+".csv"):
            self.start_date = '2019-04-22'
        else:
            try:
                with open("Public Mood/"+country+".csv",newline='') as mood_file:
                    reader = list(csv.reader(mood_file))

                last_line = reader[-1]
                print(last_line[0])
            except:
                traceback.print_exc()

if __name__ == "__main__":
    app = Sentiment_Analysis()

