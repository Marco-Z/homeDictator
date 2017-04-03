from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response, session, escape
from homeDictator.db import db_manager
from homeDictator.log import log
from homeDictator.activity import activity
from homeDictator.standings import standings
from homeDictator.user import User
from datetime import date
from subprocess import Popen
import os
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_openid import OpenID

app = Flask(__name__, template_folder="../homeDictator/templates", static_folder="../homeDictator/static")
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

#login
login_m = LoginManager()
login_m.init_app(app)
#

mydb = db_manager()

#-----
@login_m.user_loader
def load_user(a_id):
	u=db_manager().get_user_by_id(a_id)
	if u:
		user=User(a_id=u[0],nome=u[1],password=u[2],is_admin=u[3])
		return user
	return None
#----
@app.route("/", methods=['GET','POST'])
def index():
	if request.method == 'POST':
		if 'username' in session:
			print( 'Logged in as %s' % escape(session['username']))
		n = request.form['nome']
		a = request.form['attivita']
		mydb.insert(n,a,date.today())
	res = mydb.get_activities()
	attivita = activity.get_activities()
	lista_attivita = mydb.get_activities()
	punteggi = standings()
	for at in lista_attivita:
		a = at[0]
		punteggi.update(activity(a, mydb.get_times_for_activity(a)))
	nomi = mydb.retrieve_debts()
	todo = log.to_do()
	return render_template('index.html', res=res, attivita=attivita,p=punteggi,nomi=nomi,todo=todo)

@app.route("/punti/<attivita>")
def punti(attivita):
	dati = activity(attivita, mydb.get_times_for_activity(attivita))
	return render_template('punti.html',dati=dati)

@app.route("/cancella", methods=['GET','POST'])
def cancella():
	if request.method == 'POST':
		ac = request.form['attivita']
		print(ac)
		mydb.delete(ac)
		return redirect(url_for('cancella'))
	else:
		res = mydb.retrieve_all()
		lista = []
		for row in res:
			lista.append(log(row))
		return render_template('lista.html',lista=lista)

@app.route("/paga", methods=['POST'])
def paga():
	nome = request.form['nome']
	importo = float(request.form['importo'])
	desc = request.form['descrizione']
	nomi = mydb.retrieve_debts()
	paga = dict()
	somma = 0
	for n in nomi:
		paga[n[0]] = int(request.form[n[0]])
		somma = somma + paga[n[0]]
	mydb.update_credit(nome,importo)
	for n in nomi:
		mydb.update_credit(n[0],-(importo*(paga[n[0]]/somma)))
	return redirect(url_for('index'))

@app.route("/pull")
def pull():
	Popen(['./pull.bat'], shell=True,
             stdin=None, stdout=None, stderr=None, close_fds=True)
	exit(0)

@app.route('/login', methods = ['POST'])
def login():
	if request.method == 'POST':
		user = request.form['username']
		pssw=request.form['password']
		#print(mydb.update_password(user,pssw))
		#return a user ,only if the username and password are correct 
		usr= User.get_usr_by_username_and_password(username=user,password=pssw)
		print ("login in corso")
		if usr:
			print("loggato")
			login_user(usr)


	return redirect(url_for('index'))


@login_required
@app.route('/secret', methods = ['GET'])
def secret():
	print(current_user.get_id())
	return 'muschio'