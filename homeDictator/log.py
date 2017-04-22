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
		print(self.attivita)
		res = (date.today()-self.data).days >= int(self.config['intervallo'][self.attivita])
		if self.attivita == 'carta' and date.today().weekday() is not 3: #thursday
			res = False
			print('non è da fare')
		if self.attivita == 'umido' and date.today().weekday() is not 0 and date.today().weekday() is not 3: #monday or thursday
			res = False
			print('non è da fare')
		if self.attivita == 'plastica' and date.today().weekday() is not 4: #friday
			res = False
			print('non è da fare')
		if self.attivita == 'vetro' and date.today().weekday() is not 0: #monday
			res = False
			print('non è da fare')
		return res

	def to_do():
		config = configparser.ConfigParser()
		config.read('homeDictator/config.ini')
		lista = config.options('punti')
		dafare = set(lista)
		res = db_manager().retrieve_last()
		for row in res:
			activity = log(row)
			if not activity.is_old():
				dafare.remove(activity.attivita)
		try:
			dafare.remove('disordine')
		except:
			pass
		return(dafare)

