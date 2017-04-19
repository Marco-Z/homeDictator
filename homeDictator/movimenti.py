from homeDictator.db import db_manager
from datetime import date


class movimento(object):

	def __init__(self, nome, importo, descrizione, data):
		self.nome = nome
		self.importo = importo
		self.descrizione = descrizione
		self.data = data
