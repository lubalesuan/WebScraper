import requests
from bs4 import BeautifulSoup
import csv, re
import spacy, sys
from numpy import dot
from numpy.linalg import norm


# getting all job descriptions from Malaysia
def get_skill_text(output_file):
	# init write to file
	csvFile = open(output_file,'w')
	fieldnames = ['job_position', 'technology_skills', 'knowledge', 'skills']
	writer = csv.DictWriter(csvFile, fieldnames = fieldnames)
	writer.writeheader()

	career_page = requests.get("https://www.onetonline.org/find/career?c=5&g=Go")
	soup = BeautifulSoup(career_page.content, 'html.parser')
	
	# get links to job pages
	page_code_divs = soup.find_all(class_='report2ed')
	page_codes = []
	for code_div in page_code_divs:
		if code_div.find("a"):
			page_codes.append(code_div.find("a").get('href'))
	
	# get job page content
	for code in page_codes:
		job_page = requests.get(code)
		if job_page.status_code!=200:
	 		break
	 	job_soup = BeautifulSoup(job_page.content, 'html.parser')
	 	
	 	# get position name
	 	job_position = job_soup.find(class_="titleb").text
	 	job_position = re.sub("\d+-\d+\.\d+ - ","",job_position)

	 	# get technology skills
	 	technology_skills = get_technology_skills(job_soup)

	 	# get knowledge
	 	knowledge = get_short_skill(job_soup, "section_Knowledge")

	 	# get skills
	 	skills = get_short_skill(job_soup, "section_Skills")
	 	
	 	writer.writerow({'job_position':job_position, 'technology_skills':[technology_skills], 
	 		'knowledge':[knowledge], 'skills': [skills]})


# getting title and description of technological skills
def get_technology_skills(job_soup):
	more_info = get_more_info(job_soup, "section_TechnologySkills")
	if more_info != None:
		technology_skills = more_info.text.encode("utf-8").replace("\n","").replace("\xe2\x80\x94",";").split(" ; ")
		return technology_skills
	return []

# for these skills it is enough to get their title
def get_short_skill(job_soup, class_name):
	more_info = get_more_info(job_soup, class_name)
	if more_info != None:
		knowledge = [b.text.encode("utf-8") for b in more_info.find_all('b')]
		return knowledge
	return []

# get section text
def get_more_info(job_soup, class_name):
 	section = job_soup.find_all(class_=class_name)
 	if len(section)>1:
 		# tech skills description
 		if section[1].find(class_='moreinfo'):
 			more_info = section[1].find(class_='moreinfo')
 			return more_info
 	else:
 		return None

def main(argv):
	output_file = argv[1]
	get_skill_text(output_file)


if __name__ == "__main__":
	main(sys.argv)


