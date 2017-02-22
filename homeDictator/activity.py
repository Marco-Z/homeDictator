from homeDictator.db import db_manager
import configparser
from datetime import date

class activity(object):

	def __init__(self, attivita, dati):
		self.attivita = attivita
		self.volte = {}
		for riga in dati:
			self.volte[riga[0]] = riga[1]

