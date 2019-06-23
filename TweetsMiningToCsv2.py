
#  -*- coding: utf-8 -*-
import time
import tweepy
import jsonpickle
import json
import csv, traceback, os

# consumer_key = "fUQPJu7goniR2hfi5R5Klwtrn"  # new Key Data Retriveal
# consumer_secret = "JpApHOlXEfBxqoGggPZux6kRhLSnLAHhcMRq12K6yiXsUS86qf"  # new Key Data Retriveal
# access_token = "1003222000523993089-6QBWMQBTNtiVz7NrtcBw3PTigQlpjJ"
# access_token_secret = "rRrKrD5W7LhmwminPcQHzGJJei5D22xnnvfEJcxONTsEn"


class TweetToCsv():
    def __init__(self):
        self.init_twitter_api()
        self.init_dates()
        self.main()

    def writeToCsvPerDay(self):
        csvData = ['Date', 'Tweet', 'Country']
        self.csv_name = 'Tweets By Days/'+str(self.start_date)+'.csv'
        print ('Writing file '+self.csv_name)
        ret_val = self.handle_file_name()
        if ret_val == -1:
            print("File already exists, moving on")
            return
        with open(self.csv_name, 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(csvData)
            searchQuery = 'place:96683cc9126741d1'  # USA Code
            # The twitter Search API allows up to 100 tweets per query
            text_set = set()
            while (1):
                try:
                    for tweet in tweepy.Cursor(self.api.search, q=searchQuery,since = '2019-06-21', until=self.until_date).items():
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
                                writer.writerow(row)
                                if len(text_set) >= 800:
                                    return
                except:
                    print("Time out error caught.")
                    traceback.print_exc()
                    continue

    def addonDays(self, a, x):
       ret = time.strftime("%Y-%m-%d",time.localtime(time.mktime(time.strptime(a,"%Y-%m-%d"))+x*3600*24+3600))
       return ret

    def handle_file_name(self):
        if not os.path.isdir(self.folder_name):
            print('No such dir ' +self.folder_name)
            exit(1)
        if os.path.isfile(self.csv_name):
            return -1
        if not os.path.isfile(self.csv_name):
            print(f'No such file {self.csv_name} Creating it' )
            f = open(self.csv_name,'w')
            f.close()

    def init_twitter_api(self):
        consumer_key = "8h2gg259CNETqZNR9xq3Z1u3X"  # new Key Data Retriveal
        consumer_secret = "TVv2tjVSmJJzMRpyWkbW4k3A2lDoSTPbXioRbtmobPPKVHytyP"  # new Key Data Retriveal
        access_token = "1003222000523993089-nN73BpEgT4T80q8argxts6trocQAva"
        access_token_secret = "p0DlLZK9AmJjrYq4fBhJBzhMbmytvG2HvAMfUwgQFqUrV"
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

    def init_dates(self):
        self.today_date = time.strftime("%Y-%m-%d")
        self.folder_name = 'Tweets By Days'
        self.days_to_add = 1
        self.start_date = self.addonDays(self.today_date, -9)
        self.until_date = self.addonDays(self.start_date, 1)

    def main(self):
        while(self.addonDays(self.start_date,-1) != self.today_date ):
            self.writeToCsvPerDay()
            self.start_date = self.addonDays(self.start_date, 1)
            self.until_date = self.addonDays(self.until_date, 1)


if __name__ == "__main__":
    window = TweetToCsv()