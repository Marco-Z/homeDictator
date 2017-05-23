import sqlite3
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

default_password="pbkdf2:sha256:50000$bS6FggcU$6a995088dbbd98a95a1f308cd26f6610deb835db613dcdc740ec06907b40a391"
default_avatar= open('homeDictator/static/img/avatar.jpg','rb').read() 


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
			id INTEGER PRIMARY KEY AUTOINCREMENT, 
			nome TEXT NOT NULL UNIQUE, 
			credito REAL DEFAULT 0 );
			""" 

		self.cursor.execute(create_users)
		self.connection.commit()##da rifare con un form di registrazione
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

	def upgrade(self):
		sql="PRAGMA user_version"
		version =self.cursor.execute(sql).fetchone()[0]
		if version == 0:
			try:
				self.connection.commit()
				self.cursor.execute("begin transaction")
				self.cursor.execute('ALTER TABLE users ADD COLUMN password TEXT DEFAULT "%s"'%(default_password))
				self.cursor.execute('ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0;')
				self.cursor.execute('ALTER TABLE users ADD COLUMN avatar BLOB')
				self.cursor.execute("PRAGMA user_version=1")
				version =self.cursor.execute("PRAGMA user_version").fetchone()[0]
				self.connection.commit()
				print("\n","UPGRADE SUCCESFULLY TO DB VERSION %s"%(version),"\n")
			except:
				self.cursor.execute("rollback")
				print("\n","FAILED TO UPGRADE DB TO VERSION 1.0","\n")

		if version == 1:
			try:
				self.connection.commit()
				self.cursor.execute("begin transaction")
				self.cursor.execute("""
					CREATE TABLE IF NOT EXISTS groups (
					id integer PRIMARY KEY autoincrement,
					nome text NOT NULL);
						""")	
						#had to create new table to add new foreign key, so create a new one, copy the data and delete the old one			
				self.cursor.execute("""
					CREATE TABLE IF NOT EXISTS user_back ( 
					id INTEGER PRIMARY KEY AUTOINCREMENT, 
					nome TEXT NOT NULL UNIQUE, 
					credito REAL DEFAULT 0, 
					password TEXT DEFAULT "%s" , 
					is_admin INTEGER DEFAULT 0,
					avatar BLOB ,
					group_id INT REFERENCES groups(id));
					""" %(default_password))
				self.cursor.execute("""insert into user_back (id,nome,credito,password,is_admin,avatar) 
					select id,nome,credito,password,is_admin,avatar from users""")
				self.cursor.execute("DROP TABLE users")
				self.cursor.execute("ALTER TABLE user_back RENAME TO users")
				self.cursor.execute("PRAGMA user_version=2")
				version =self.cursor.execute("PRAGMA user_version").fetchone()[0]
				self.connection.commit()
				print("\n","UPGRADE SUCCESFULLY TO DB VERSION %s"%(version),"\n")
			except:
				self.cursor.execute("rollback")
				print("\n","FAILED TO UPGRADE DB TO VERSION 2","\n")

		

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
	def get_user_by_id(self,a_id):
		select_command = """
			SELECT id,nome,password,is_admin
			FROM users
			WHERE id = ?
			"""
		try:
			return self.cursor.execute(select_command,[a_id]).fetchone()
		
		except:
			return None

	def retrieve_movimenti(self):
		select_command = """
			SELECT * FROM movimenti ORDER BY data DESC;
			"""
		res = self.cursor.execute(select_command).fetchall()
		return res
	def update_password(self,a_id,old_pword,new_pword):
		try:
			select_command = """
			SELECT  password 
			FROM users
			WHERE id = ?
			"""
			res=self.cursor.execute(select_command, [a_id]).fetchone()[0]
			if check_password_hash(res,old_pword):
				update_command = """
				UPDATE users
				SET password = ?
				WHERE id = ? ;
				"""
				self.cursor.execute(update_command,[generate_password_hash(new_pword), a_id])
				self.connection.commit()
				return True
		except:
			return False

	def insert_user(self, nome, password, is_admin):
			insert_command = """
				INSERT INTO users (nome, password,is_admin) 
				VALUES (?,?,?);
				"""
			self.cursor.execute(insert_command,[nome, password, is_admin])
			self.connection.commit()

	def get_user_from_name_and_password(self, nome,password):
		select_command = """
			SELECT id, nome, password , is_admin 
			FROM users
			WHERE nome = ?
			"""
		res=self.cursor.execute(select_command, [nome]).fetchone()
		if res:
			if check_password_hash(res[2],password):
				return res
		return None

	def change_avatar(self, image, a_id):
		blob=None
		try:
			blob=image.read()
			sql="update users set avatar = ? where id = ? " 
			res=self.cursor.execute(sql, [sqlite3.Binary(blob),a_id]) 
			self.connection.commit()
			return True
		except Exception as e:
			print("error while %s was changing avatar" %(a_id) )
			return False
		else:
			return False

	def get_avatar_from_name(self,nome):
		try:
			sql="select avatar from users where nome = ?" 
			res=self.cursor.execute(sql, [nome]).fetchone()[0] 
			if res:
				return res
			else:
				return default_avatar
		except :
			print("error while retriving %s's avatar" %(nome) )
			return default_avatar

	def is_useradmin(self,id):
		try:
			sql="select is_admin from users where id = ?"
			res=self.cursor.execute(sql, [id]).fetchone()[0]
			if res==0:
				return False
			else:
				return True
		except :
			return False

	def get_userGroupId(self,userid):
		try:
			sql="select group_id from users where id = ?"
			res=self.cursor.execute(sql, [userid]).fetchone()[0]
			return res
		except :
			return None
	def get_GroupName(self,userid):
		try:
			sql="select nome from groups where id = ?"
			res=self.cursor.execute(sql, [group_id]).fetchone()[0]
			return res
		except :
			return None

	def getGroupsAndComponents(self,group_id):#non ancora usato
		#return a dict of touple as: key =groupid value={(groupname,[componentsname..])}
		try:
			groups={}
			sql="select groups.id,groups.nome,users.nome from users join groups on group_id=groups.id "
			res=self.cursor.execute(sql).fetchAll()
			for row in res:
				group[row[0]]=(row[1],group[row[0]][1]+[row[3]])
			return res
		except :
			return None

	def get_GroupComponentsname(self, group_id):
		try:
			components=[]
			sql="select users.nome from users where group_id=?"
			res=self.cursor.execute(sql, [group_id]).fetchAll()
			for row in res:
				components.append(row[0])
			return components
		except :
			return None
	def add_Group(self, nome):
		try:
			sql="insert into groups (nome) values ?"
			res=self.cursor.execute(sql, [nome])
			self.connection.commit()
			return True
		except Exception as e:
			return False

	def set_UserGroup(self, user_id,group_id):
		try:
			sql="update users set group_id = ? where id=?"
			res=self.cursor.execute(sql, [group_id,user_id])
			self.connection.commit()
			return True
		except Exception as e:
			return False
