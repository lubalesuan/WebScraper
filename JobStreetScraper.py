import requests
from bs4 import BeautifulSoup


class ScrapeJobStreet:

	def getSkillText(self):
		alphabetPages = requests.get("https://www.jobstreet.com.my/en/career-insights/all-roles/browse-a")
		soup = BeautifulSoup(alphabetPages.content, 'html.parser')
		divs = soup.find_all(class_="_1xl_o")
		for div in divs:
			endUrl = div.find("a").get('href')
			url = "https://www.jobstreet.com.my"+endUrl
			print url
			# jobPage = requests.get(url)
			# jobPageSoup = BeautifulSoup(jobPage.content, 'html.parser')


	
scraper = ScrapeJobStreet()
scraper.getSkillText()