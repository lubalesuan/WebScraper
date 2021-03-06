import requests
from bs4 import BeautifulSoup
import csv, re
import sys
from numpy import dot
from numpy.linalg import norm


# getting all job descriptions from Malaysia
def get_skill_text(source_page, output_file):
	# init write to file
	csvFile = open(output_file,'w')
	fieldnames = ['job_position', 'technology_skills', 'knowledge', 'skills']
	writer = csv.DictWriter(csvFile, fieldnames = fieldnames)
	writer.writeheader()

	# get page that has links to all job pages
	career_page = requests.get(source_page)
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
		# if job_page.status_code!=200:
	 # 		break
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
	 	
	 	# output skills
	 	output_skills(writer, job_position, technology_skills, knowledge, skills)



# getting title and description of technological skills
def get_technology_skills(job_soup):
	more_info = get_more_info(job_soup, "section_TechnologySkills")
	if more_info != None:
		technology_skills = more_info.text.encode("utf-8").replace("\n","").replace("\xe2\x80\x94",";").split(";")
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



# print skills to file
def output_skills(writer, job_position, technology_skills, knowledge, skills):
	# writing arrays line by line, rather than in 1 row
 	max_length = max(len(skills), len(technology_skills), len(knowledge))

	for i in range(0,max_length):
 		tech_sk = knowledge_sk = skill_sk = ""

 		# get skill one by one
 		if len(technology_skills)>i:
 			tech_sk = technology_skills[i]
 		if len(skills)>i:
 			skill_sk = skills[i]
 		if len(knowledge)>i:
 			knowledge_sk = knowledge[i]

 		# print job position on first iteration
 		if i == 0:
 			writer.writerow({'job_position':job_position, 'technology_skills':tech_sk, 
 		'knowledge':knowledge_sk, 'skills': skill_sk})
 		# omit printing job position on all other iterations
 		else:
			writer.writerow({'job_position':'','technology_skills': tech_sk, 
 		'knowledge': knowledge_sk, 'skills': skill_sk})

# get positions from csv file
def get_positions(source, dest):
	with open(source) as csvFile:
		reader = csv.DictReader(csvFile)
		pos_list = ""
		for row in reader:
			pos_list += row['job_position']+", "
		print(pos_list)


def main(argv):
	output_file = argv[2] #file to which print scraped data
	source_page = argv[1] #page from which to scrape job positions
	get_skill_text(source_page, output_file)


if __name__ == "__main__":
	main(sys.argv)


