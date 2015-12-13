#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import csv
import re
import os
import argparse
import logging
import config

from logging.handlers import RotatingFileHandler
from datetime import datetime

# This has to be done before importing Tweet from Django in order
# to avoir a Django error

#TODO GENERAL:
#    - Faire le nettoyage de donnees
#    - Gerer les unicode.....
#    - Decoder les tweet.text sortantes

os.environ['DJANGO_SETTINGS_MODULE'] = 'tweetlearn.tweetlearn.settings'
from tweetlearn.tweets.models import Tweet

class TweetLearn():

    def __init__(self):

        # Recherche des credentials via le ConfigParser
        self.cfg = config.Config()
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
	self.clean_tweet(tweet)

        with open(config.CLEANED_CSV, 'a+') as csvfile:
            csv_writer = csv.writer(csvfile)
	    # TODO: 
            #csv_writer.writerow([str(tweet.id), tweet.user.name, tweet.text, str(tweet.created_at)])
            csv_writer.writerow([str(tweet.id), tweet.user.name, tweet.text, str(tweet.created_at, -1)]) # -1 car non annote
	    self.logger.info("Tweet (%d) has been added to csv" % tweet.id)
       
    def save_tweet_orm(self, tweet):

	# Save a tweet into the Django's ORM
	# TODO:
	# Check comment auto incrementer l'id
	# Mettre en parametres les tweet.texts
	# Changer le date=date_today

	self.clean_tweet(tweet)
	date_today = datetime.date(datetime.now())
	
	tweet_test = Tweet(id=tweet.id,
			   user=tweet.user.name, 
                           text=tweet.text, 
                           date=date_today,
                           category=-1) # TODO: -1 car le tweet n'est pas encore annote (USELESS?)
	tweet_test.save()
	self.logger.info("Tweet (%d) has been added to the orm" % tweet.id)

	
    def save_tweets_orm(self, tweets):
    	for tweet in tweets:
	    self.save_tweet_orm(tweet)

    def save_tweets_csv(self, tweets):
	for tweet in tweets:
            self.save_tweet_csv(tweet)

    def clean_tweet(self, tweet):
	
	if type(tweet.text) is str:
	    # Le nettoyage a deja ete effectue
	    return

	tweet.text = tweet.text.encode("utf8")
	tweet.user.name = tweet.user.name.encode("utf8")
	
	# TODO:
	# A perfectionner
	diez = re.compile("#(\w+)")
	arobase = re.compile("@(\w+)")
	rt = re.compile("RT")
	url = re.compile("https://")
	
	tweet.text = diez.sub("\\1", tweet.text)
	tweet.text = arobase.sub("", tweet.text)
	tweet.text = rt.sub("", tweet.text)
	tweet.text = url.sub("", tweet.text)
        print tweet.text
	
if __name__ == "__main__":

    t = TweetLearn()
    # print(type(t.get_home_timeline()))
    tweet = "RT @RAPELITE: .@sethgueko .@Geogioxv3 s'inventent https://blablabla.com"

    diez = re.compile("#(\w+)")
    arobase = re.compile("\.?@(\w+):?")
    rt = re.compile("RT")
    url = re.compile("https://")
    
    tweet = diez.sub("\\1", tweet)
    tweet = arobase.sub("", tweet)
    tweet = rt.sub("", tweet)
    tweet = url.sub("", tweet)

    print tweet
   
