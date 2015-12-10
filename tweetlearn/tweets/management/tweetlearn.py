#!/usr/bin/env python
# coding: utf-8
import tweepy
import ConfigParser
import argparse
import config
import csv
import re

FILE = "db.csv"
f = open(FILE, "a")

CONFIG = config.Config()
PARSER = argparse.ArgumentParser(description='Parsing of the app')
PARSER.add_argument('--proxy', help="The app will use the Lille1's proxy", action='store_true', dest='proxy')

auth = tweepy.OAuthHandler(consumer_key=CONFIG['consumer_key'],
		         consumer_secret=CONFIG['consumer_secret'])
auth.set_access_token(key=CONFIG['access_token_key'],
		      secret=CONFIG['access_token_secret'])

args = PARSER.parse_args()
if args.proxy:
	api = tweepy.API(auth, proxy='cache-etu.univ-lille1.fr:3128')
else:
	api = tweepy.API(auth)

public_tweets = api.home_timeline()

writer = csv.writer(f)
writer.writerow(('id', 'user', 'text', 'date', 'request'))

if __name__ == "__main__":
	cfg = config.Config()
	regex = re.compile(r"@(\w)*", re.IGNORECASE)
	regex_dollars = re.compile(r"$(\d \.)*", re.IGNORECASE)

	for tweet in public_tweets:
		print "[id]:", tweet.id
		user_name = tweet.user.name.encode("utf-8")
		print "[user]:", user_name
		tweet.text = unicode(tweet.text)
		print type(tweet.text)
		txt = tweet.text.encode("utf-8")
		print "text_OLD:", txt
		txt = regex.sub("@USERNAME", txt)
		print "text_OLDbis", txt
		txt = regex_dollars.sub("$XXX", txt)
		print type(txt)
		
		print "[text]:", txt
		print "[date]:", tweet.created_at
		print "______"
		writer.writerow((tweet.id, user_name, txt, tweet.created_at, "no request"))

f.close()

	
		

