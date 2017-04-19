import sqlite3
from datetime import datetime, date

class db_manager(object):

	def __init__(self):
		self.connection = sqlite3.connect("homeDictator/my.db")
		self.cursor = self.connection.cursor()

	def create(self):

		# initialize log table
		create_command = """
			CREATE TABLE IF NOT EXISTS log ( 
			id INTEGER PRIMARY KEY, 
			nome TEXT, 
			attivita TEXT, 
			data TEXT);
			"""
		self.cursor.execute(create_command)

		# initialize users table
		create_users = """
			CREATE TABLE IF NOT EXISTS users ( 
			id INTEGER PRIMARY KEY, 
			nome TEXT, 
			credito REAL DEFAULT 0);
			"""
		self.cursor.execute(create_users)
		self.connection.commit()
		if len(self.cursor.execute("SELECT * FROM users;").fetchall()) == 0:
			self.cursor.execute('INSERT INTO users (nome) VALUES ("Marco")')
			self.cursor.execute('INSERT INTO users (nome) VALUES ("Matteo")')
			self.cursor.execute('INSERT INTO users (nome) VALUES ("Maurizio")')
			self.cursor.execute('INSERT INTO users (nome) VALUES ("Nicola")')
			self.connection.commit()

		# initialize cost table
		create_command = """
			CREATE TABLE IF NOT EXISTS cost ( 
			id INTEGER PRIMARY KEY, 
			creditore TEXT, 
			importo REAL, 
			data TEXT, 
			descrizione TEXT);
			"""
		self.cursor.execute(create_command)

		# initialize movimenti table
		create_command = """
			CREATE TABLE IF NOT EXISTS movimenti ( 
			id INTEGER PRIMARY KEY, 
			nome TEXT, 
			importo REAL, 
			descrizione TEXT, 
			data TEXT);
			"""
		self.cursor.execute(create_command)

	def reset(self):
		delete_command = """
			DELETE FROM log;
			"""
		self.cursor.execute(delete_command)
		delete_users = """
			DELETE FROM users;
			"""
		self.cursor.execute(delete_users)
		self.connection.commit()

	def insert(self, nome, attivita, data):
		insert_command = """
			INSERT INTO log (nome, attivita, data) 
			VALUES (?,?,?);
			"""
		self.cursor.execute(insert_command,[nome, attivita, data])
		self.connection.commit()

	def delete(self, a_id):
		insert_command = """
			DELETE FROM log WHERE id=?;
			"""
		self.cursor.execute(insert_command,[a_id])
		self.connection.commit()

	def retrieve_all(self):
		select_command = """
			SELECT * FROM log ORDER BY data DESC;
			"""
		res = self.cursor.execute(select_command)
		return res

	def retrieve_last(self):
		select_command = """
			SELECT id, nome, attivita, MAX(data) AS data
			FROM log
			GROUP BY attivita
			ORDER BY data DESC;
			"""
		return self.cursor.execute(select_command)

	def retrieve_debts(self):
		select_command = "SELECT nome, credito FROM users;"
		return self.cursor.execute(select_command).fetchall()

	def update_credit(self,nome,importo):
		print(self.cursor.execute("SELECT nome, credito FROM users WHERE nome = (?)",[nome]).fetchone())
		update_command = """
			UPDATE users
			SET credito = credito + (?)
			WHERE nome = (?);
			"""
		self.cursor.execute(update_command,[importo, nome])
		self.connection.commit()
		print(self.cursor.execute("SELECT nome, credito FROM users WHERE nome = (?)",[nome]).fetchone())

	def get_activities(self):
		select_command = """
			SELECT DISTINCT attivita
			FROM log;
			"""
		return list(self.cursor.execute(select_command))

	def get_times_for_activity(self, attivita):
		select_command = """
			SELECT nome, count(nome) AS volte
			FROM log
			WHERE attivita = ?
			GROUP BY nome
			"""
		return self.cursor.execute(select_command, [attivita])

	def string_to_date(date):
		return datetime.strptime(date, '%Y-%m-%d').date()

	def logga_movimento(self, nome, importo, descrizione):
		insert_command = """
			INSERT INTO movimenti (nome, importo, descrizione, data) 
			VALUES (?,?,?,?);
			"""
		self.cursor.execute(insert_command,[nome, importo, descrizione, date.today()])
		self.connection.commit()

	def retrieve_movimenti(self):
		select_command = """
			SELECT * FROM movimenti ORDER BY data DESC;
			"""
		res = self.cursor.execute(select_command).fetchall()
		return res