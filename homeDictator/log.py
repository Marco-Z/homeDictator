from homeDictator.db import db_manager
import configparser
from datetime import date

class log(object):

	def __init__(self, row):
		self.a_id = row[0]
		self.nome = row[1]
		self.attivita = row[2]
		self.data = db_manager.string_to_date(row[3])
		self.config = configparser.ConfigParser()
		self.config.read('homeDictator/config.ini')

	def is_old(self):
		return(date.today()-self.data).days >= int(self.config['intervallo'][self.attivita])

	def to_do():
		res = db_manager().retrieve_last()
		lista = []
		for row in res:
			activity = log(row)
			if activity.is_old():
				lista.append(activity)
		return lista