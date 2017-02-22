from homeDictator.db import db_manager
import configparser
from datetime import date

class log(object):

	def __init__(self, row):
		self.nome = row[0]
		self.attivita = row[1]
		self.data = db_manager.string_to_date(row[2])
		self.config = configparser.ConfigParser()
		self.config.read('homeDictator/config.ini')

	def __str__(self):
		return self.nome + ' ' + self.attivita + ' ' + str(self.data)

	def is_old(self):
		return(date.today()-self.data).days >= int(self.config['intervallo'][self.attivita])
