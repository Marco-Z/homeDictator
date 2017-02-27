import sqlite3
from datetime import datetime, date

class db_manager(object):

	def __init__(self):
		self.connection = sqlite3.connect("homeDictator/my.db")
		self.cursor = self.connection.cursor()

	def create(self):
		create_command = """
			CREATE TABLE IF NOT EXISTS log ( 
			id INTEGER PRIMARY KEY, 
			nome TEXT, 
			attivita TEXT, 
			data TEXT);
			"""
		self.cursor.execute(create_command)
		self.connection.commit()

	def reset(self):
		delete_command = """
			DELETE FROM log;
			"""
		self.cursor.execute(delete_command)
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
			SELECT * FROM log;
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

	def get_activities(self):
		select_command = """
			SELECT DISTINCT attivita
			FROM log;
			"""
		return list(self.cursor.execute(select_command))

	def get_names(self):
		select_command = """
			SELECT DISTINCT nome
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

