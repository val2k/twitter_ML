#!/usr/bin/env python 
import tweepy
import csv
import os
from config import Config
from datetime import datetime

# This has to be done before importing Tweet from Django in order
# to avoir a Django error

os.environ['DJANGO_SETTINGS_MODULE'] = 'tweetlearn.tweetlearn.settings'
from tweetlearn.tweets.models import Tweet

# from ... { chemin vers le model Django } import Tweet

#auth = tweepy.OAuthHandler(consumer_key='MKbGv7ijw2HRx8XGTcu7nArDM',
#		  consumer_secret='xmWacwRxkxe9nGYFWuJLoliqG4fXqFP47cicqm58vhRlD7YVCk')
#auth.set_access_token(key='293610000-n5bU4mDlZXLNjk2EwGiH3wNNYjCP0Yf730Urtxa0',
#		     secret='MGwMQVzFiX5iEUOLjo7IiSOon631GmUXLF2cQ1hZzU38A')
#api = tweepy.API(auth, proxy='cache-etu.univ-lille1.fr:3128')
#public_tweets = api.home_timeline()

class TweetLearn():

    def __init__(self):
        # Recherche des credentials via le ConfigParser
        # 
        self.cfg = Config()
        self.api = self.init_api()
    
    def init_api(self):
        pass
    
    def get_home_timeline(self):
        return self.api.home_timeline()
    	
    def save_into_csv(self):
        with open(self.cfg.csv, 'wb') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['TEST', 'TEST2'])
       
    def push_into_orm(self):
        pass
    	
    def save_tweet(self):
	# Check comment auto incrementer l'id
	date_today = datetime.date(datetime.now())
	tweet_test = Tweet(user="blazazabla", text="lazazol", date=date_today, category=-1)
	tweet_test.save()

if __name__ == "__main__":

    t = TweetLearn()
    t.save_into_csv()
    t.save_tweet()
    #for tweet in public_tweets:
    #	print "[id]: ", tweet.id
    #	print "[user]: ", tweet.user.name
    #	print "[text]: ", tweet.text
    #	print "[date]: ", tweet.created_at
    #	print "______"

