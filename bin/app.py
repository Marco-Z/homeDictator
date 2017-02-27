from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from homeDictator.db import db_manager
from homeDictator.log import log
from homeDictator.activity import activity
from homeDictator.standings import standings
from datetime import date

app = Flask(__name__, template_folder="../homeDictator/templates", static_folder="../homeDictator/static")

mydb = db_manager()

@app.route("/", methods=['GET','POST'])
def index():
	if request.method == 'POST':
		n = request.form['nome']
		a = request.form['attivita']
		mydb.insert(n,a,date.today())
	res = mydb.retrieve_last()
	lista = []
	for row in res:
		lista.append(log(row))
	res = mydb.get_activities()
	attivita = activity.get_activities()
	lista_attivita = mydb.get_activities()
	punteggi = standings()
	for at in lista_attivita:
		a = at[0]
		punteggi.update(activity(a, mydb.get_times_for_activity(a)))
	return render_template('index.html', lista=lista, res=res, attivita=attivita,p=punteggi)

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
		return redirect(url_for('index'))
	else:
		res = mydb.retrieve_all()
		lista = []
		for row in res:
			lista.append(log(row))
		return render_template('lista.html',lista=lista)
