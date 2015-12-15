#!/usr/bin/env python
import ConfigParser
 
CONFIGFILE = 'cfg/config.ini'
POSITIVE_FILE = 'words/positive.txt'
NEGATIVE_FILE = 'words/negative.txt'
CLEANED_CSV = 'csv/cleaned_tweets.csv'
ANNOTATED_CSV = 'csv/annotated_tweets.csv'

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

    def get_csv(self, nom):
        return self.cfg.get(csv, name)

