from homeDictator.db import db_manager
import configparser

class Group(object):
	def __init__(self, a_id, name="",components=[]):
		self.a_id = a_id
		if not name:
			self.name=db_manager.get_GroupName(self.name)
		else:
			self.name = name
		if not components:
			self.components=db_manager.get_GroupComponentsname(self.components)
		else:
			self.components=components

	def get_id(self):
		return int(self.a_id)

	def get_name(self):
		return str(self.name)

	def get_components(self):
		return self.components

	def set_name(self,name):
		self.name = name

	def set_components(self,components):
		self.components= components

	def get(a_id):
		try: 
			group =Group(a_id)
			if not group.get_name:
				return None
			else:
				return group
		except:
			print ('errore nel caricamento dell\'utente')
			return None 

	def add_to_db(self):
   		return db_manager().add_Group(self.nome, self.components)