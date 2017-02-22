from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from homeDictator.db import db_manager
from homeDictator.log import log
from homeDictator.activity import activity
from homeDictator.standings import standings
from datetime import date

app = Flask(__name__, template_folder="../homeDictator/templates")

mydb = db_manager()

@app.route("/")
def index():
	res = mydb.retrieve_last()
	lista = []
	for row in res:
		lista.append(log(row))
	res = mydb.get_activities()
	return render_template('index.html', lista=lista, res=res)

@app.route("/punti/<attivita>")
def punti(attivita):
	dati = activity(attivita, mydb.get_times_for_activity(attivita))
	return render_template('punti.html',dati=dati)

@app.route("/classifica")
def classifica():
	lista_attivita = mydb.get_activities()
	punteggi = standings()
	for attivita in lista_attivita:
		a = attivita[0]
		punteggi.update(activity(a, mydb.get_times_for_activity(a)))
	return render_template('classifica.html',p=punteggi)

@app.route("/aggiungi", methods=['GET', 'POST'])
def aggiungi():
	if request.method == 'GET':
		nomi = mydb.get_names()
		attivita = mydb.get_activities()
		return render_template('aggiungi.html', nomi=nomi, attivita=attivita)
	else:
		n = request.form['nome']
		a = request.form['attivita']
		mydb.insert(n,a,date.today())
		return redirect(url_for('index'))
