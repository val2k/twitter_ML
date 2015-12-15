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


# This has to be done before importing Tweet from Django in order
# to avoid a Django error

os.environ['DJANGO_SETTINGS_MODULE'] = 'tweetlearn.tweetlearn.settings'
from tweets.models import Tweet

class TweetLearn():

    def __init__(self, proxy=False):
	
        self.cfg = config.Config()
        self.api = self.init_api(proxy)
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
	    (deprecated)
	"""

	parser = argparse.ArgumentParser(description='Parser')
	parser.add_argument("--proxylille1", dest="proxylille1",
                            action="store_true",
                            help="Use or not the Lille1's proxy")
	args = parser.parse_args()
	return args

    def init_api(self, proxylille1=False):
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

	if proxylille1:
	    proxy = self.cfg.get_proxy('proxylille1')
	    api = tweepy.API(auth, proxy=proxy)
	else:
	    api = tweepy.API(auth)

	return api
    
    def get_home_timeline(self):
        return self.api.home_timeline()
    	
    def search(self, request):
	return self.api.search(request, lang="fr")

    def save_tweet_csv(self, tweet, request):
	""" Ajoute un tweet dans le fichier CSV des tweets nettoyes et annotes
	    : tweet   : tuple (TweetObject, category), tweet a ajouter au fichier
	    : request : requete ayant permis la recuperation du tweet
	"""

	tweet, category = tweet
	self.clean_tweet(tweet)

        with open(config.ANNOTATED_CSV, 'a+') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([str(tweet.id), str(tweet.user.name), str(tweet.text), str(tweet.created_at), request, category]) 
	    self.logger.info("Tweet (%d) has been added to csv" % tweet.id)
       
    def save_tweet_orm(self, tweet, request):
		
	""" Ajoute un tweet dans l'ORM de Django
	    : tweet   : tuple (TweetObject, category, tweet a ajouter au fichier
	    : requete : requete ayant permis la recuperation du tweet
		    
	"""

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
    	for tweet in tweets:
	    self.save_tweet_orm(tweet, request)

    def save_tweets_csv(self, tweets, request):
	for tweet in tweets:
            self.save_tweet_csv(tweet, request)

    def clean_tweet(self, tweet):
	""" Nettoyage d'un tweet
	    : tweet : (TwwetObject), tweet a nettoyer
	"""
	
	if type(tweet.text) is str:
	    # Le nettoyage a deja ete effectue
	    return

	tweet.text = tweet.text.encode("utf8")
	tweet.user.name = tweet.user.name.encode("utf8")
	
	# TODO:
	# A perfectionner: caraceters etranger unicode ?

	diez = re.compile("#(\w+)")
	arobase = re.compile("@(\w+):?")
	rt = re.compile("RT")
	url = re.compile("(http)s*:*/*/*t*(.)*c*o*/*[a-zA-Z0-9]*")
	ret = re.compile("\n")
	e_accent = re.compile("é|è|ê|ë");
	a_accent = re.compile("à|â|ä");
	i_accent = re.compile("î|ï|ì");
	o_accent = re.compile("ô|ö|ò");
	nombre = re.compile("[0-9]+[0-9]*")
	

	tweet.text = diez.sub("\\1", tweet.text)
	tweet.text = arobase.sub("", tweet.text)
	tweet.text = rt.sub("", tweet.text)
	tweet.text = url.sub("", tweet.text)
	tweet.text = e_accent.sub("e", tweet.text)
	tweet.text = a_accent.sub("a", tweet.text)
	tweet.text = i_accent.sub("i", tweet.text)
	tweet.text = o_accent.sub("o", tweet.text)
	tweet.text = ret.sub("", tweet.text)
	
    def process_classif(self, algo, request, freq=False, big=False):
	""" Methode d'entree pour la classification avec les divers algos
	    : algo    : algo utilise pour la classification
	    : request : requete ayant permis de recuperer les tweets
	    : freq    : boolean pour l'algo Bayes (classification en presence / frequence)
	    : big     : boolean pour l'algo Bayes (classification unigramme / bigramme)
	"""

        algos = ('KNN', 'Bayes', 'Keyword')
	request = request.encode("utf8")

	if algo not in algos:
	    return

	tweets = self.search(request)	

	returned_tweets = []

	for tweet in tweets:
	    self.clean_tweet(tweet)
	
	    if algo == "Bayes":
	        data = self.alg.classifier_bayes(tweet, freq, big)
	        tweet = self.save_tweet_orm(data, request)
	        self.save_tweet_csv(data, request)
	        returned_tweets.append(tweet)
	    elif algo == "Keyword":
	        data = self.alg.classifier_keyw(tweet)
	        tweet = self.save_tweet_orm(data, request)
	        self.save_tweet_csv(data, request)
	        returned_tweets.append(tweet)
	    elif algo == "KNN":
		# TODO: k doit etre parametrable
		k = 10
	        data = self.alg.classifier_KNN(tweet, k)
	        tweet = self.save_tweet_orm(data, request)
	        self.save_tweet_csv(data, request)
	        returned_tweets.append(tweet)
	
	return returned_tweets
