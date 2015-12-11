#!/usr/bin/env python
import ConfigParser
 
CONFIGFILE = 'cfg/config.ini'
POSITIVE_FILE = 'tweets/positive.txt'
NEGATIVE_FILE = 'tweets/negative.txt'
CLEANED_CSV = 'cleaned_tweets.csv'
ANNOTATED_CSV = 'annotated_tweets.csv'

class Config:

    def __init__(self):
	self.cfg = ConfigParser.RawConfigParser()
	self.cfg.read(CONFIGFILE)

    def get_credential(self, name):

	try:
	    credential = self.cfg.get('credentials', name)
	except ConfigParser.NoOptionError:
            # TODO: logger
            print("Error while retrieving the credential: %s" % name)
	else:
	    return self.cfg.get('credentials', name)

    def get_proxy(self, proxyname):

	proxy = self.cfg.get(proxyname, 'proxy')
	return proxy

    def get_csv(self):
	# Return the name of the cfg file
        return self.cfg.get(csv, name)

