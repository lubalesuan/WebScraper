# WebScraper
### Author: Luba Le Xuan
#### What it does?
Scrapes major Malayisan job sites for publicly available data on job skills.
#### Sites used:
JobStreet, Indeed
#### Structure and functions explained:
__JobStreetScraper.py:__
1. downloads all pages for jobs available in Malaysia (from JobStreet career insights)
2. scrapes pages for job position name and job skills
3. inserts scraped data into jobStreet.csv
4. counts skill frequency across job positions
5. sorts skills by popularity

__jobStreet.csv:__

list of job positions and skills important for those

__IndeedScraper.py:__
1. downloads all pages for jobs available in Malaysia
2. scrapes pages for job position names and job descriptions
3. inserts scraped data into indeedRaw.csv
4. extracts keywords from job descriptions

__IndeedRaw.csv:__

list of job positions and their job descriptions

#### Resources and tutorials used:
NLP made easy using spacy: https://www.analyticsvidhya.com/blog/2017/04/natural-language-processing-made-easy-using-spacy-%e2%80%8bin-python/