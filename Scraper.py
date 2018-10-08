class Scraper:

	def __init__(self, rawFileName, fieldnames):
		self.csvFile = open(rawFileName,'w')
		self.fieldnames = fieldnames
		self.writer = csv.DictWriter(csvFile, fieldnames = fieldnames)
		writer.writeheader()

	def stripText(self, filename):
		
	