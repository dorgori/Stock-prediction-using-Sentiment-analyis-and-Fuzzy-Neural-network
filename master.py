

import TweetsMiningToCsv
import create_clean_tweets
import sentiAnalysis
import StockMinningToCsv
import traceback

class Master():
    try:
        print('Gather tweets, it may take time depends on how many days missing')
        TweetsMiningToCsv.TweetToCsv()
        print('Done collect tweets ! \nNlp stage started')
        create_clean_tweets.NLP()
        print('Done Nlp !\n Start sentiment analysis, it may take time')
        sentiAnalysis.Sentiment_Analysis()
        print('Done sentiment analysis !\nStart collecting stock values')
        StockMinningToCsv.StockValues()
        print('Done collect stock values\n')
        print("Ready to predict")
    except:
        traceback.print_exc()
