from bin.app import app
from homeDictator.db import db_manager
from datetime import date

mydb = db_manager()
mydb.create()
mydb.upgrade()

app.run(host='0.0.0.0')