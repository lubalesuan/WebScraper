# WebScraper
### Author: Luba Le Xuan
#### What it does?
Scrapes major Malayisan job sites for publicly available data on job skills.
#### Sites used:
JobStreet, Indeed
#### Structure and functions explained:
JobStreetScraper.py:
	1) downloads all pages for jobs available in Malaysia (from JobStreet career insights)
	2) scrapes pages for job position name and job skills
	3) inserts scraped data into jobStreet.csv
	3) counts skill frequency across job positions
	4) sorts skills by popularity
jobStreet.csv:
	list of job positions and skills important for those
IndeedScraper.py:
	1) downloads all pages for jobs available in Malaysia
	2) scrapes pages for job position names and job descriptions
	3) inserts scraped data into indeedRaw.csv
	4) extracts keywords from job descriptions
	

