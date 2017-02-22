from nose.tools import *
from homeDictator.db import db_manager
from datetime import date

def test_db_init():
	try:
		mydb = db_manager()
	except e:
		pass
	assert_true(mydb is not None)

def test_db_reset():
	mydb = db_manager()
	mydb.create()
	mydb.reset()
	assert_true(len(list(mydb.retrieve_all())) is 0)
	mydb.insert('testoh', 'landsat', date.today())
	mydb.reset()
	assert_true(len(list(mydb.retrieve_all())) is 0)

def test_insertion_retrieval():
	mydb = db_manager()
	mydb.create()
	mydb.reset()
	mydb.insert('testoh', 'landsat', date.today())
	res = mydb.retrieve_all()
	assert_true(len(list(res)) is 1)
	for row in res:
		assert_true(type(row[1]) is str)
		assert_true(len(row[1]) > 0)
		assert_true(type(row[2]) is str)
		assert_true(len(row[2]) > 0)
		assert_true(type(row[3]) is str)
		assert_true(len(row[3]) > 0)

	# mydb.insert('', '', '')
	# for row in res:
	# 	assert_true(type(row[1]) is str)
	# 	assert_true(type(row[2]) is str)
	# 	assert_true(type(row[3]) is str)
	# 	assert_true(len(row[3]) > 0)
	# 	print(row)

	mydb.reset()


def test_date_conversion():
	mydb = db_manager()
	mydb.create()
	mydb.reset()
	mydb.insert('testoh', 'landsat', date.today())
	print(date.today)
	res = mydb.retrieve_all()
	for row in res:
		assert_true(db_manager.string_to_date(row[3]) == date.today())
	mydb.reset()