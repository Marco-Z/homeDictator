from homeDictator.db import db_manager
import configparser

class User(object):

	def __init__(self, a_id, nome,password, is_admin):
		self.a_id = a_id
		self.password = password
		self.username = nome
		self.is_admin = is_admin

	def is_authenticated(self):
		return True


	def is_active(self):
		return True


	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.a_id)

	def get(a_id):
		try: 
			user=User(db_manager().get_user(a_id))
			return (User(a_id=user[0],nome=user[1], password=user[2],is_admin=user[3]))
		except:
			return None 

	def add_to_db(self):
   		db_manager().insert_user(self.nome, self.password, self.is_admin)


	def get_usr_by_username_and_password(username, password):
		usr=db_manager().get_user_from_name_and_password(nome=username,password=password)
		if usr:
			user=User(
			a_id=usr[0],
			nome=usr[1],
			password=usr[2],
			is_admin=usr[3])
			return user
		else:
			return None
