from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from homeDictator.db import db_manager
from homeDictator.log import log
from homeDictator.activity import activity
from homeDictator.standings import standings
from homeDictator.spesa import spesa
from datetime import date
from subprocess import Popen

app = Flask(__name__, template_folder="../homeDictator/templates", static_folder="../homeDictator/static")

mydb = db_manager()

@app.route("/", methods=['GET','POST'])
def index():
	if request.method == 'POST':
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

@app.route("/spesa", methods=['GET','POST'])
def la_spesa():
	s = spesa()
	if request.method == 'POST':
		testoh = request.form['spesa']
		s.scrivi(testoh)
		return redirect(url_for('index'))
	else:
		testoh = s.leggi()
		return render_template('spesa.html',testoh=testoh)

