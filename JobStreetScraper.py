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
				# if job skills found on page
				if jobPageSoup.find_all(class_="_1dAEn"):
					skills = jobPageSoup.find_all(class_="_1dAEn")[0].find_all(class_="_1eKnr")
					jobPosition = jobPageSoup.find("span",class_="_189iV").text
					skillRow = [jobPosition]
					for skill in skills:
						skillRow.append(skill.text)
					writer.writerow(skillRow)
			# csvFile.close()



scraper = ScrapeJobStreet()
scraper.getSkillText()