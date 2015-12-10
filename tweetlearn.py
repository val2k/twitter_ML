#!/usr/bin/env python 
import tweepy
import csv
import os
import argparse

from config import Config
from datetime import datetime

# This has to be done before importing Tweet from Django in order
# to avoir a Django error

os.environ['DJANGO_SETTINGS_MODULE'] = 'tweetlearn.tweetlearn.settings'
from tweetlearn.tweets.models import Tweet

class TweetLearn():

    def __init__(self):

        # Recherche des credentials via le ConfigParser
        self.cfg = Config()
	self.args_parser = self.init_parser()
        self.api = self.init_api()
    
    def init_parser(self):

	parser = argparse.ArgumentParser(description='Parser')
	parser.add_argument("--proxylille1", dest="proxylille1",
                            action="store_true",
                            help="Use or not the Lille1's proxy")
	args = parser.parse_args()
	return args

    def init_api(self):

	consumer_key = self.cfg.get_credential('consumer_key')
	consumer_secret = self.cfg.get_credential('consumer_secret')
	access_key = self.cfg.get_credential('access_token_key')
	access_secret = self.cfg.get_credential('access_token_secret')
	
        auth = tweepy.OAuthHandler(consumer_key=consumer_key,
                                   consumer_secret=consumer_secret)
	auth.set_access_token(key=access_key,
                              secret=access_secret)
	if self.args_parser.proxylille1:
	    proxy = self.cfg.get_proxy('proxylille1')
	    api = tweepy.API(auth, proxy=proxy)
	else:
	    api = tweepy.API(auth)

	return api
    
    def get_home_timeline(self):
        return self.api.home_timeline()
    	
    def save_into_csv(self):
	# TODO:
	# Add a tweet o the CSV file 
        with open(self.cfg.csv, 'wb') as csvfile:
            csv_writer = csv.writer(csvfile)
	    # TODO: 
            csv_writer.writerow(['TEST', 'TEST2'])
       
    def save_into_orm(self):

	# Save a tweet into the Django's ORM
	# TODO:
	# Check comment auto incrementer l'id
	# Mettre en parametres les datas
	date_today = datetime.date(datetime.now())
	tweet_test = Tweet(user="blazazabla", 
                           text="lazazol", 
                           date=date_today,
                            category=-1)
	tweet_test.save()

if __name__ == "__main__":

    t = TweetLearn()
    t.save_into_csv()
    t.save_into_orm()

    #for tweet in public_tweets:
    #	print "[id]: ", tweet.id
    #	print "[user]: ", tweet.user.name
    #	print "[text]: ", tweet.text
    #	print "[date]: ", tweet.created_at
    #	print "______"

