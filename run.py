from bin.app import app
from homeDictator.db import db_manager
from datetime import date

# mydb = db_manager()
# mydb.create()

# mydb.insert('testoh', 'landsat', date.today())
# mydb.insert('testohh', 'lendsat', date.today())
# mydb.insert('testoh!', 'explosion', date.today())

app.run()