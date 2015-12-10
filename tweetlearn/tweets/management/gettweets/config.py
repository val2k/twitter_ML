import ConfigParser


class Config():

	def __init__(self):
		self.cfg = ConfigParser.RawConfigParser()
		self.cfg.readfp(open("config.ini", "ra"))
		self.cfgs = {}
		self.inflate()
	
	def __getitem__(self, attribute):
		return self.cfgs[attribute] 

	def inflate(self):
		self.cfgs['consumer_key'] = self.cfg.get('credentials', 'consumer_key')
		self.cfgs['consumer_secret'] = self.cfg.get('credentials', 'consumer_secret')
		self.cfgs['access_token_key'] = self.cfg.get('credentials', 'access_token_key')
		self.cfgs['access_token_secret'] = self.cfg.get('credentials', 'access_token_secret')

