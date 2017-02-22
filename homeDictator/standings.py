from homeDictator.db import db_manager
import configparser
import collections

class standings(object):

	def __init__(self):
		self.punteggi = {}
		self.config = configparser.ConfigParser()

	def _add_points(self, nome, volte, attivita):
		self.config.read('homeDictator/config.ini')
		valore = int(self.config['punti'][attivita])
		try:
			self.punteggi[nome]
		except KeyError:
			self.punteggi[nome] = int(volte)*valore
		else:
			self.punteggi[nome] = int(self.punteggi[nome]) + int(volte)*valore

	def update(self, attivita):
		for nome in attivita.volte:
			self._add_points(nome,attivita.volte[nome],attivita.attivita)
		MyDict = self.punteggi
		WantedOutput = sorted(MyDict, key=lambda x : MyDict[x], reverse=True)
		p = collections.OrderedDict()
		for nome in WantedOutput:
			p[nome] = self.punteggi[nome]
		self.punteggi = p
