import requests
from bs4 import BeautifulSoup
import csv
from string import ascii_lowercase

class ScrapeJobStreet:

	# getting all job skills for Malaysia
	def getSkillText(self):
		# init write to file
		csvFile = open('data/jobStreet.csv','w')
		fieldnames = ['job_position', 'skills']
		writer = csv.DictWriter(csvFile, fieldnames = fieldnames)
		writer.writeheader()
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
					skillRow = ",".join([skill.text for skill in skills])
					writer.writerow({'job_position':jobPosition, 'skills':skillRow})

	def countSkills(self):
		skillDict = dict()
		with open('data/jobStreet.csv') as csvfile:
			reader = csv.DictReader(csvfile)
			# iterate through csv file rows
			for row in reader:
				# iterate through skills
				skillArray = row['skills'].split(",")
				for skill in skillArray:
					if skillDict.has_key(skill):
						# increment count of skills
						skillDict[skill] +=1
					else:
						# if doesn't contain key, init count to 1
						skillDict[skill] = 1
		return skillDict

	def getPopularSkills(self, n=1, skillDict=None):
		popularSkills = []
		if skillDict is None:
			return None
		sorted_by_value = sorted(skillDict.items(), key=lambda kv: kv[1])[::-1]
		for i in range(0,n):
			popularSkills.append(sorted_by_value[i])
		return popularSkills

scraper = ScrapeJobStreet()
# scraper.getSkillText()
skillDict = scraper.countSkills()
sortedSkills = scraper.getPopularSkills(len(skillDict), skillDict)
resultFile = open('data/jobStreetSorted.csv','w')
resultFieldnames = ["skill", "count"]
resultWriter =  csv.DictWriter(resultFile, fieldnames = resultFieldnames)
for i in sortedSkills:
	resultWriter.writerow({"skill":i[0],"count":i[1]})

