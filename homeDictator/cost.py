from homeDictator.db import db_manager
from datetime import date


class log(object):

	def __init__(self, row):
		self.a_id = row[0]
		self.nome = row[1]
		self.attivita = row[2]
		self.data = db_manager.string_to_date(row[3])
		self.config = configparser.ConfigParser()
		self.config.read('homeDictator/config.ini')