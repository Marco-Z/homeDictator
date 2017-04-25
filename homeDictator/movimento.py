from homeDictator.db import db_manager

class movimento(object):

	def __init__(self, mov):
		self.nome = mov[1]
		self.importo = float(mov[2])
		self.descrizione = mov[3]
		self.data = db_manager.string_to_date(mov[4])
