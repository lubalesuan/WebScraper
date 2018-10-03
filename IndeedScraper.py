import requests
from bs4 import BeautifulSoup
import csv

class IndeedScraper:

	# getting all job descriptions from Malaysia
	def getSkillText(self):
		pageNext = True
				# init write to file
		csvFile = open('data/indeedRaw.csv','w')
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
				pageNext = false
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
				# print jobDescription
				# insert data in csv file
				writer.writerow({'job_position':jobPosition,'job_description':jobDescription})



scraper = IndeedScraper()
scraper.getSkillText()