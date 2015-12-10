#!/usr/bin/env python
import ConfigParser
 
PATH_TO_CONFIGFILE = 'cfg/config.ini'

class Config:
    def __init__(self):
	self.csv = 'db.csv'
	self.cfg = ConfigParser.RawConfigParser()
	self.cfg.read(PATH_TO_CONFIGFILE)

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

if __name__ == "__main__":
	cfg = Config()
	print(cfg.get_credential('consum_key'))
	print cfg.cfg
