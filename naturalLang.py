import nltk
import html
import csv
from html.parser import HTMLParser
import re


def naturalLanguage(sentence):
    emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    ch = "\\x"  #replace \xfdsda to @
    sentence = str(sentence.encode('utf-8'))
    sentence = sentence.replace(ch, "@")
    sentence = html.unescape(sentence)  # unescape HTML
    sentence = re.sub(r"http\S+", "", sentence)  # remove normal URLS
    sentence = re.sub(r"pic\.twitter\.com/\S+", "", sentence)  # remove pic.twitter.com URLS
    sentence = re.sub(r"@\S+", "", sentence)  # remove User Tags
    sentence = re.sub(emoji_pattern, '', sentence) #remove emojis
    return sentence[4:]


with open('tweets.csv',  newline='') as csvFile:
    reader = list(csv.reader(csvFile))
    csvFile.close()

    twts = []
    cnt=0
    for row in reader:
        row[1] = naturalLanguage(row[1])
        if not row[1].isspace():
            twts.append(row)

with open('pureTweets.csv', 'w', newline='') as pureTweets:
    writer = csv.writer(pureTweets)
    writer.writerows(twts)
    pureTweets.close()

