import requests
from bs4 import BeautifulSoup

class IndeedScraper:
	def getSkillText(self):
		pageNext = True
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
				pageNext = false
				break
			soup = BeautifulSoup(page.content, 'html.parser')
			divs = soup.find_all(class_='jobtitle')
			for div in divs:
				endUrl = div.find("a").get('href')
				url = "https://www.indeed.com.my"+endUrl
				jobPage = requests.get(url)
				jobPageSoup = BeautifulSoup(jobPage.content, 'html.parser')

scraper = IndeedScraper()
scraper.getSkillText()