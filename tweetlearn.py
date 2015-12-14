#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import csv
import re
import os
import argparse
import logging
import config
import alg

from logging.handlers import RotatingFileHandler
from datetime import datetime


#TODO GENERAL:
#    - (Faire le nettoyage de donnees)
#    - (Decoder les tweet.text sortantes)
#    - Faire

# This has to be done before importing Tweet from Django in order
# to avoid a Django error

os.environ['DJANGO_SETTINGS_MODULE'] = 'tweetlearn.tweetlearn.settings'
from tweetlearn.tweets.models import Tweet

class TweetLearn():

    def __init__(self):

        self.cfg = config.Config()
	self.args_parser = self.init_parser()
        self.api = self.init_api()
	self.logger = logging.getLogger()
	self.init_logger()
	self.alg = alg.Algos()

    def init_logger(self):
	""" Initialisation du logger
	"""

	self.logger.setLevel(logging.DEBUG)
	formatter = logging.Formatter("%(asctime)s :: %(levelname)s :: %(message)s")
	file_handler = RotatingFileHandler('app.log', 'a', 100000)
	file_handler.setLevel(logging.DEBUG)

	steam_handler = logging.StreamHandler()
	steam_handler.setLevel(logging.DEBUG)
	self.logger.addHandler(steam_handler)
    
    def init_parser(self):
	""" Initialisation du parser
	"""

	parser = argparse.ArgumentParser(description='Parser')
	parser.add_argument("--proxylille1", dest="proxylille1",
                            action="store_true",
                            help="Use or not the Lille1's proxy")
	args = parser.parse_args()
	return args

    def init_api(self):
	""" Initialisation de l'API, les infos de connexion sont
	    recuperes dans un fichier de configuration
	"""

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
    	
    def search(self, request):
	return self.api.search(request)

    def save_tweet_csv(self, tweet, request):
	""" Ajoute un tweet dans le fichier CSV des tweets nettoyes mais
	    non annotes
	    @tweet: tweet a ajouter au fichier
	"""

	self.clean_tweet(tweet)

        with open(config.CLEANED_CSV, 'a+') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([str(tweet.id), tweet.user.name, tweet.text, str(tweet.created_at), request, -1]) # -1 car non annote
	    self.logger.info("Tweet (%d) has been added to csv" % tweet.id)
       
    def save_tweet_orm(self, tweet, request):
		
	""" Ajoute un tweet dans l'ORM de Django
	    @tweet: tuple comprenenant le tweet a ajouter a l'ORM (objet retourne)
		    par tweepy, ainsi que sa catégorie
		    
	"""
	# TODO:
	# Mettre en parametres les tweet.text (???)
	# Changer le date=date_today (!!!!)

	tweet, category = tweet
	self.clean_tweet(tweet)
	date_today = datetime.date(datetime.now())
	
	returned_tweet = Tweet(id=tweet.id,
			   user=tweet.user.name, 
                           text=tweet.text, 
                           date=date_today,
		           request=request,
                           category=category) 
	returned_tweet.save()
	self.logger.info("Tweet (%d) has been added to the orm" % tweet.id)
	return returned_tweet

	
    def save_tweets_orm(self, tweets, request):
	""" Ajoute plusieurs tweets à l'ORM 
	"""
    	for tweet in tweets:
	    self.save_tweet_orm(tweet, request)

    def save_tweets_csv(self, tweets, request):
	""" Ajoute plusieurs tweets au fichier CSV
	"""
	for tweet in tweets:
            self.save_tweet_csv(tweet, request)

    def clean_tweet(self, tweet):
	
	if type(tweet.text) is str:
	    # Le nettoyage a deja ete effectue
	    return

	tweet.text = tweet.text.encode("utf8")
	tweet.user.name = tweet.user.name.encode("utf8")
	
	# TODO:
	# A perfectionner, surtout pour l'URL

	diez = re.compile("#(\w+)")
	arobase = re.compile("@(\w+)")
	rt = re.compile("RT")
	#url = re.compile("/^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2, 6})([\/\w \.-]*)*\/?$/") #TODO: OK ?
	url = re.compile("(https?:\/\/)?[(\w\.-]*")

	tweet.text = diez.sub("\\1", tweet.text)
	tweet.text = arobase.sub("", tweet.text)
	tweet.text = rt.sub("", tweet.text)
	tweet.text = url.sub("", tweet.text)
	
    def process_classif(self, algo, request):
        algos = ('KNN', 'Bayes')

	if algo not in algos:
	    return
	tweets = self.search(request)	
	self.save_tweets_csv(tweets, request)

	returned_tweets = []

	for tweet in tweets:
	    data = self.alg.classifier(tweet)
	    tweet = self.save_tweet_orm(data, request)
	    print("tweet:", tweet)
	    returned_tweets.append(tweet)

	return returned_tweets
	
if __name__ == "__main__":

    t = TweetLearn()
    print(t.process_classif('KNN', 'lepen'))
    

    # Test du cleaning
    #tweet = "RT @RAPELITE: .@sethgueko .@Geogioxv3 s'inventent https://blablabla.com"

    #diez = re.compile("#(\w+)")
    #arobase = re.compile("\.?@(\w+):?")
    #rt = re.compile("RT")
    #url = re.compile("https://")
    #
    #tweet = diez.sub("\\1", tweet)
    #tweet = arobase.sub("", tweet)
    #tweet = rt.sub("", tweet)
    #tweet = url.sub("", tweet)

