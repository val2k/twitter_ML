from __future__ import absolute_import

from django.core.management.base import BaseCommand, CommandError
from tweets.models import Tweet

from ..gettweets import config

import tweepy
import ConfigParser
import argparse
import csv
import re


class Command(BaseCommand):

	help = "Retrieve tweets with specified request"

	def __init__(self, *args, **kwargs):
		super(Command, self).__init__(*args, **kwargs)
		
		self.cfg = config.Config()
		self.auth = self.initialize_auth()
		self.writer = self.initialize_writer()


	def add_arguments(self, parser):

		parser.add_argument('-n', 
			nargs='+',
			type=int, 
			default=50, 
			dest='nb_tweets')
		parser.add_argument('--proxylille1',
			action='store_true',
			dest='proxylilleun',
			default=False,
			help="Set Lille 1's proxy")
		parser.add_argument('--request',
			dest='request',
			default='timeline',
			type=str)


	def handle(self, *args, **options):

		proxy = ''
		if options['proxylilleun']:
			# todo: mettre le proxy dans la cfg
			proxy = 'cache-etu.univ-lille1.fr:3128'		

		self.api = tweepy.API(self.auth, proxy=proxy)
		self.requests = self.initialize_requests()
		
		tweets = self._get_tweets(options['request'])
		self.print_tweets(tweets, options['request'])
		self.add_to_csv(tweets, options['request'])


	def _get_tweets(self, request):
		
		if request in self.requests:
			return self.requests[request]
		else:
			# todo: 
			raise Exception("todo: requete non supportee")
		

	def print_tweets(self, tweets, request):
	
		for tweet in tweets:
			print("[id]: %d" % tweet.id)
			print("[date]: %s" % tweet.created_at)
			print("[user]: %s" % tweet.user.name.encode('utf-8'))
			print("[request]: %s" % request)
			print("[text]: %s" % tweet.text.encode('utf-8'))
			print("=====================================")


	def add_to_csv(self, tweets, request):

		regex_username = re.compile(r"@(\w)*", re.IGNORECASE)
		regex_dollar = re.compile(r"$(\d \.)*", re.IGNORECASE)

		for tweet in tweets:

			tweet_text = tweet.user.name.encode('utf-8')
			tweet_text = regex_username.sub("@USERNAME", tweet_text)
			tweet_text = regex_dollar.sub("$XXX", tweet_text)

			self.writer.writerow(
				(tweet.id, 
				 tweet.created_at,
				 tweet_text,
				 request,
				 tweet.text.encode('utf-8')
				)	
			)


	# todo: mettre les initializes avec _
	def initialize_writer(self):

		# todo: mettre dans la cfg	
		file = 'tweets.csv'
		return csv.writer(open(file, "a"))
		

	def initialize_requests(self):
		
		requests = {}
		requests['timeline'] = self.api.home_timeline()

		return requests
	

	def initialize_auth(self):

		auth = tweepy.OAuthHandler(
			consumer_key=self.cfg['consumer_key'],
		      	consumer_secret=self.cfg['consumer_secret'])
		auth.set_access_token(
		      	key=self.cfg['access_token_key'],
		      	secret=self.cfg['access_token_secret'])
		
		return auth


	def add_arguments(self, parser):

		parser.add_argument('-n', 
			nargs='+',
			type=int, 
			default=50, 
			dest='nb_tweets')
		parser.add_argument('--proxylille1',
			action='store_true',
			dest='proxylilleun',
			default=False,
			help="Set Lille 1's proxy")
		parser.add_argument('--request',
			dest='request',
			default='timeline',
			type=str)
			

