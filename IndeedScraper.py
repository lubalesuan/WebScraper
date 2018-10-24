import requests
from bs4 import BeautifulSoup
import csv
import spacy
from numpy import dot
from numpy.linalg import norm

class IndeedScraper:

	# getting all job descriptions from Malaysia
	def getSkillText(self, outputFilename):
		# init write to file
		csvFile = open(outputFilename,'w')
		fieldnames = ['job_position', 'job_description']
		writer = csv.DictWriter(csvFile, fieldnames = fieldnames)

		for i in range(0,19):
			beginUrl = "https://www.indeed.com.my/jobs?q=&l=Malaysia&limit=50"
			endUrl = ""
			# get url for pages
			if i!=0:
				endUrl="&start="+str(i*50)
			url = beginUrl+endUrl
			page = requests.get(url)
			#  if page doesn't exist, stop iterating
			if page.status_code!=200:
				break
			soup = BeautifulSoup(page.content, 'html.parser')
			divs = soup.find_all(class_='jobtitle')
			for div in divs:
				endUrl = div.find("a").get('href')
				url = "https://www.indeed.com.my"+endUrl
				# download job page
				jobPage = requests.get(url)
				jobPageSoup = BeautifulSoup(jobPage.content, 'html.parser')
				# scrape job description and job position
				jobPosition = ""
				if jobPageSoup.find(class_="jobsearch-JobInfoHeader-title"):
					jobPosition = jobPageSoup.find(class_="jobsearch-JobInfoHeader-title").text.encode("utf-8")
				jobDescription = ""
				if jobPageSoup.find(class_="jobsearch-JobComponent-description"):
					jobDescription = unicode(jobPageSoup.find(class_="jobsearch-JobComponent-description").get_text().encode("utf-8"), errors='ignore')
				# insert data in csv file
				writer.writerow({'job_position':jobPosition,'job_description':jobDescription})

	# tokenize data
	def tokenize(self, fileName, nlp):
		doc = nlp(unicode(open(fileName).read().decode('utf8')))
		return doc

	# remove noise
	def preprocessData(self, doc):
		acceptPartsOfSpeech = ["PROPN", "VERB", "NOUN", "ADJ"]
		#  remove stop words, short words, and unacceptable parts of speech
		preprocessedTokens = [token for token in doc if ((not token.is_stop) & ((token.pos_ in acceptPartsOfSpeech) & (len(token.string) > 3)))]
		return preprocessedTokens

	# find entities for tokens. Entities can be person, location, etc.
	# method just for fun, didn't call it
	def entityDetect(self, tokens):
		for token in tokens:
			if token.ent_type_:
				print token.ent_type_+", "+ token.string


	# using spacy default similarity function
	# to find tokens most relevant to searcy keywords
	# will change to pca later
	def vectorSimilarity(self, tokens, outputFilename, nlp):
		keywords = [nlp(u'job skills'), nlp(u'engineering'), nlp(u'job qualifications')]
		# tokendict key = token, value = average similarity score
		tokenDict = dict()
		for token in tokens:
			# avegSim calculates similarity score
			avegSim = 0
			for key in keywords:
				avegSim+=token.similarity(key)
			# divide to cal aveg similarity score
			if (not tokenDict.has_key(token.lemma_.lower())):
				tokenDict[token.lemma_.lower()] = avegSim/(len(keywords))
		# sort by similarity score
		sorted_by_value = sorted(tokenDict.items(), key=lambda kv: kv[1])[::-1]
		# print keywords to csv file
		fieldnames = ['keyword', 'similarity_score']
		outputFile = open(outputFilename, "w")
		writer = csv.DictWriter(outputFile, fieldnames = fieldnames)
		for token in sorted_by_value:
			writer.writerow({'keyword': token[0], 'similarity_score': str(token[1]).encode("utf-8").decode("utf-8")})

scraper = IndeedScraper()
# scraper.getSkillText()
nlp = spacy.load('en_core_web_lg')
for i in range (0,3):
	tokenized = scraper.tokenize("data/indeedRawMY"+str(i)+".csv", nlp)
	preprocessed = scraper.preprocessData(tokenized)
	scraper.vectorSimilarity(preprocessed, "data/indeedKeywordsMY"+str(i)+".csv", nlp)


