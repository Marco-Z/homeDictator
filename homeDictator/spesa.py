class spesa(object):

	def __init__(self):
		pass

	def scrivi(self, testoh):
		myfile = open('spesa.txt', 'w')
		myfile.write(testoh)
		myfile.flush()
		myfile.close()

	def leggi(self):
		myfile = open('spesa.txt', 'r')
		testoh = myfile.read()
		myfile.close()
		return testoh
		