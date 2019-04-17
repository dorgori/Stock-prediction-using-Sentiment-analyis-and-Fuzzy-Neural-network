
#  -*- coding: utf-8 -*-
import time
import tweepy
import jsonpickle
import json
consumer_key = "fUQPJu7goniR2hfi5R5Klwtrn"      #new Key Data Retriveal
consumer_secret = "JpApHOlXEfBxqoGggPZux6kRhLSnLAHhcMRq12K6yiXsUS86qf"      #new Key Data Retriveal

access_token="1003222000523993089-6QBWMQBTNtiVz7NrtcBw3PTigQlpjJ"
access_token_secret="rRrKrD5W7LhmwminPcQHzGJJei5D22xnnvfEJcxONTsEn"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

f = open("test.txt", 'w')
searchQuery = 'place:96683cc9126741d1'  # USA Code
maxTweets = 1000000

#The twitter Search API allows up to 100 tweets per query
tweetsPerQry = 100
tweetCount = 0
text_set = set()
# Tell the Cursor method that we want to use the Search API (api.search)
# Also tell Cursor our query, and the maximum number of tweets to return
while(1):
    try:
        for tweet in tweepy.Cursor(api.search, q=searchQuery).items():
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
                    f.write(date + ' ' + str(tweet_text) +' ' +' ' +full_country + '\n')
                    tweetCount += 1
    except:
        print("Time out error caught, tweetCount "+str(tweetCount))
        time.sleep(60)
        continue
f.close()