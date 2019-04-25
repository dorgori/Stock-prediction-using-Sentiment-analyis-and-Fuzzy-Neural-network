import indicoio
indicoio.config.api_key = '0b80d9da8f4e847bd018ef74e597ad62'

# single example

mylist = ["b'@mitchellvii How about reparations for all the people who, did pay their student loans."]
mylist.append("People who paid matter too! (Sarcasm obviously)'")
mylist.append("    ")
mylist.append("I love writing code!")
mylist.append("http://www.yeay.com I love writing code!")
#print(indicoio.emotion(["b'@mitchellvii How about reparations for all the people who did pay their student loans.",  "People who paid matter too! (Sarcasm obviously)'"]))
for tweet in mylist:
    print(indicoio.emotion(tweet))
print(len(mylist))