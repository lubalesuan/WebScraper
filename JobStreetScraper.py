import requests
from bs4 import BeautifulSoup
import csv
from string import ascii_lowercase

class ScrapeJobStreet:

	def getSkillText(self):
		# init write to file
		csvFile = open('jobStreet.csv','w')
		writer = csv.writer(csvFile)
		# iterate through alphabetized job pages
		for c in ascii_lowercase:
			alphabetPages = requests.get("https://www.jobstreet.com.my/en/career-insights/all-roles/browse-"+c)
			soup = BeautifulSoup(alphabetPages.content, 'html.parser')
			# get links to job pages
			divs = soup.find_all(class_="_1xl_o")
			# job page parser
			for div in divs:
				endUrl = div.find("a").get('href')
				url = "https://www.jobstreet.com.my"+endUrl
				jobPage = requests.get(url)
				jobPageSoup = BeautifulSoup(jobPage.content, 'html.parser')
				# if div with job skills found on page
				if jobPageSoup.find_all(class_="_1dAEn"):
					# get skills
					skills = jobPageSoup.find_all(class_="_1dAEn")[0].find_all(class_="_1eKnr")
					jobPosition = jobPageSoup.find("span",class_="_189iV").text
					# insert job position in csv row
					skillRow = [jobPosition]
					# insert skills in csv row
					for skill in skills:
						skillRow.append(skill.text)
					writer.writerow(skillRow)

	def analyzeSkills(self):
		popularSkillsDict = dict()
		with open('jobStreet.csv') as csvfile:
			reader = csv.DictReader(csvfile)
			# iterate through csv file rows
			for row in reader:
				# iterate through skills
				for x in range (1, len(row)):
					print row.keys()
					# if popularSkillsDict.has_key(row[x]):
					# 	# increment count of skills
					# 	popularSkillsDict[row[x]] +=1
					# else:
					# 	# if doesn't contain key, init count to 1
					# 	popularSkillsDict[row[x]] = 1
		print popularSkillsDict


scraper = ScrapeJobStreet()
# scraper.getSkillText()
scraper.analyzeSkills()


