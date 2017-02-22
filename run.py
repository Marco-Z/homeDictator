from bin.app import app
from homeDictator.db import db_manager
from datetime import date

mydb = db_manager()
mydb.create()

app.run()