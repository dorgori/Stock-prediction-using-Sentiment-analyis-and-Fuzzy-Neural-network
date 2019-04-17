
import time
import tweepy

consumer_key = "8h2gg259CNETqZNR9xq3Z1u3X"      #new Key Data Retriveal
consumer_secret = "TVv2tjVSmJJzMRpyWkbW4k3A2lDoSTPbXioRbtmobPPKVHytyP"      #new Key Data Retriveal

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token="1003222000523993089-nN73BpEgT4T80q8argxts6trocQAva"
access_token_secret="p0DlLZK9AmJjrYq4fBhJBzhMbmytvG2HvAMfUwgQFqUrV"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
print(api.me().name)
# The Twitter user who we want to get tweets from
name = "Xbox"
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
c = tweepy.Cursor(api.followers, id=name).items()
file = open("xbox_file.txt" , 'w')
i = 0

for user in tweepy.Cursor(api.followers, id = name).items():
    try:
        if(user.location != ""):
            i= i + 1
            print(i)
        file.write(user.screen_name.encode(encoding="utf-8", errors="strict")
            +";"+ '%1s' % user.location.encode(encoding="utf-8", errors="strict")
            +";"+ '%1s' % str(user.created_at)
            +";"+ '%1s' % str(user.followers_count) + '\n')
        time.sleep(0.5)
    except:
        print("Time out error caught.")
        time.sleep(60)
        continue
file.close()
