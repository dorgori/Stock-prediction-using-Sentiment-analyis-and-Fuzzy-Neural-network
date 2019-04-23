
#  -*- coding: utf-8 -*-
import time
import tweepy
import jsonpickle
import json
import csv
consumer_key = "8h2gg259CNETqZNR9xq3Z1u3X"      #new Key Data Retriveal
consumer_secret = "TVv2tjVSmJJzMRpyWkbW4k3A2lDoSTPbXioRbtmobPPKVHytyP"      #new Key Data Retriveal

access_token="1003222000523993089-nN73BpEgT4T80q8argxts6trocQAva"
access_token_secret="p0DlLZK9AmJjrYq4fBhJBzhMbmytvG2HvAMfUwgQFqUrV"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
#api = tweepy.API(auth)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

#f = open("test23.txt", 'w')
'''
Write into csv file
'''
csvData = ['Date', 'Tweet', 'Country']
with open('tweets.csv', 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(csvData)

    searchQuery = 'place:96683cc9126741d1'  # USA Code
    maxTweets = 1000000

    #The twitter Search API allows up to 100 tweets per query
    tweetsPerQry = 100
    tweetCount = 0
    text_set = set()
    while(1):
        try:
            for tweet in tweepy.Cursor(api.search, q=searchQuery).items(maxTweets):
                # Verify the tweet has place info before writing (It should, if it got past our place filter)
                if tweet.place is not None:
                    # Encode as JSON format
                    tweet_data = (jsonpickle.encode(tweet._json, unpicklable=False))
                    d = json.loads(tweet_data)
                    full_country = d['place']['full_name']
                    date = d['created_at']
                    tweet_text = str(d['text']).encode('utf-8', errors="strict")
                    if tweet_text not in text_set:
                        text_set.add(tweet_text)
                        row = []
                        row.append(date)
                        row.append(str(tweet_text))
                        row.append(full_country)
                        if writer.writerow(row):
                            print('success!')
                        tweetCount += 1
        except:
            print("Time out error caught."+str(tweetCount))
            time.sleep(60)
            continue
    csvFile.close()