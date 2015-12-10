#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import csv
import os
import argparse
import logging

from logging.handlers import RotatingFileHandler
from config import Config
from datetime import datetime

# This has to be done before importing Tweet from Django in order
# to avoir a Django error

#TODO GENERAL:
#    - Faire le nettoyage de donnees
#    - Gerer les unicode.....

os.environ['DJANGO_SETTINGS_MODULE'] = 'tweetlearn.tweetlearn.settings'
from tweetlearn.tweets.models import Tweet

class TweetLearn():

    def __init__(self):

        # Recherche des credentials via le ConfigParser
        self.cfg = Config()
	self.args_parser = self.init_parser()
        self.api = self.init_api()
	self.logger = logging.getLogger()
	self.init_logger()

    def init_logger(self):
	self.logger.setLevel(logging.DEBUG)
	formatter = logging.Formatter("%(asctime)s :: %(levelname)s :: %(message)s")
	file_handler = RotatingFileHandler('app.log', 'a', 100000)
	file_handler.setLevel(logging.DEBUG)

	steam_handler = logging.StreamHandler()
	steam_handler.setLevel(logging.DEBUG)
	self.logger.addHandler(steam_handler)
    
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
    	
    def save_tweet_csv(self, tweet):
	# TODO:
	# Add a tweet o the CSV file 
        with open(self.cfg.csv, 'wb') as csvfile:
            csv_writer = csv.writer(csvfile)
	    # TODO: 
	    tweet_username = tweet.user.name.encode("utf8")
	    tweet_text = tweet.text.encode("utf8")
            #csv_writer.writerow([str(tweet.id), tweet.user.name, tweet.text, str(tweet.created_at)])
            csv_writer.writerow([str(tweet.id), tweet_username, tweet_text, str(tweet.created_at)])
	    self.logger.info("Tweet (%d) has been added to csv" % tweet.id)
       
    def save_tweet_orm(self, tweet):

	# Save a tweet into the Django's ORM
	# TODO:
	# Check comment auto incrementer l'id
	# Mettre en parametres les datas
	date_today = datetime.date(datetime.now())
	user = tweet.user.name.encode("utf8")
	text = tweet.text.encode("utf8")
	
	tweet_test = Tweet(id=tweet.id,
			   user=user, 
                           text=text, 
                           date=date_today,
                           category=-1)
	tweet_test.save()
	self.logger.info("Tweet (%d) has been added to the orm" % tweet.id)

	
    def save_tweets_orms(self, tweets):
    	for tweet in tweets:
	    save_tweet_orm(tweet)

    def save_tweets_csv(self, tweets):
	for tweet in tweets:
            save_tweet_csv(tweet)

	

if __name__ == "__main__":

    t = TweetLearn()
    # print(type(t.get_home_timeline()))

    public_tweets = t.get_home_timeline()
    for tweet in public_tweets:
	t.save_tweet_csv(tweet)
	t.save_tweet_orm(tweet)
    	print "[id]: ", tweet.id
    	print "[user]: ", tweet.user.name
    	print "[text]: ", tweet.text
    	print "[date]: ", tweet.created_at
    	print "______"

