import json
import csv, os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 \
    import Features, EntitiesOptions, KeywordsOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-11-16',
    iam_apikey='Eqp-hGGlHDvTChx2YAIXmp31IHtjEk4PgkCv6oAfBjGd',
    url='https://gateway-lon.watsonplatform.net/natural-language-understanding/api'
)

with open('Csv By Days/California/2019-04-22.csv', newline='') as tweetsFile:
    lst = list(csv.reader(tweetsFile))
tweetsFile.close()
list = []
lst.remove(lst[0])
for tweet in lst:
    list.append(tweet[1])
for tweet in list:
    response = natural_language_understanding.analyze(
        text=
        tweet,
        features=Features(
            entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
            keywords=KeywordsOptions(emotion=True, sentiment=True))).get_result()

    '''
    The results of emotions in: response['entities'][0]['emotion']
    The classify if Positive/Natural/Negative in : response['entities'][0]['sentiment']
    '''

    print(json.dumps(response, indent=2))