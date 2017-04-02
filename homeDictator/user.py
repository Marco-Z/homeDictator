from homeDictator.db import db_manager
import configparser

class User(object):
	a_id = ""
	password = ""
	username = ""
	is_admin = ""

	def __init__(self, a_id, nome,password, is_admin):

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.id)  # python 2
		except NameError:
			return str(self.id)

	@classmethod
	def get(a_id):
		try: 
			user=User(db_manager().get_user(a_id))
			return (User(a_id=user[0],nome=user[1], password=user[2],is_admin=user[3]))
		except:
			return None 
