import indicoio
import csv
indicoio.config.api_key = '0b80d9da8f4e847bd018ef74e597ad62'

# single example
# print(indicoio.emotion(tweet))

def classification(file_name):
    with open(file_name, newline='') as tweetsFile:
        reader = list(csv.reader(tweetsFile))
    tweetsFile.close()

    emotions_classification = []
    i=0
    for row in reader:
        if i == 10:
            break
        emotions_classification.append(indicoio.emotion(row[1]))
        i+=1

    return emotions_classification

emo = ['anger', 'sadness', 'fear', 'joy', 'surprise']

def main():
        emotions = classification("Csv_countries/California.csv")
        i = 0
        dailyDictionary = {'anger': 0, 'sadness': 0, 'fear': 0, 'joy': 0, 'surprise': 0}
        for val in emotions:
            dailyDictionary['joy'] += val['joy']
            dailyDictionary['anger'] += val['anger']
            dailyDictionary['sadness'] += val['sadness']
            dailyDictionary['fear'] += val['fear']
            dailyDictionary['surprise'] += val['surprise']

        print (dailyDictionary) #dictionary before normalize
        key_max = max(dailyDictionary.keys(), key=(lambda k: dailyDictionary[k]))
        ###max_value = dailyDictionary[key_max]
        dict_sum = sum(dailyDictionary.values())
        normalizelist = list(map(lambda v: v/dict_sum, dailyDictionary.values()))

        for i, val in enumerate(emo):
            dailyDictionary[val] = normalizelist[i]
        print(dailyDictionary)  #dictionary after normalize


if __name__ == "__main__":
    main()

