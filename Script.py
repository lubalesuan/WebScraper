import sys, csv, random

# prints out a list of job positions from csv file
# params: source = csv file
# ATTENTION: random shuffle, not in order
def get_positions(source_list, dest):
	output_file = open(dest, 'w')
	pos_list = []
	# print(source_list)
	# print(output_file)
	for source in source_list:
		with open(source) as csvFile:
			reader = csv.DictReader(csvFile)
			for row in reader:
				if len(row['job_position']) > 0:
					pos_list.append(row['job_position'].lower())
	# random_list = pos_list[:]
	random.shuffle(pos_list)
	# print(pos_list)
	pos_string = ", ".join(pos_list)
	output_file.write(pos_string)


if __name__ == "__main__":
	# if user wants to print positions from csv file,
	# where job positions are in first column
	# call prit_positions
	if sys.argv[1] == "get_positions":
		# get a list of source files
		source_list = sys.argv[2:len(sys.argv)-1]
		output_file = sys.argv[len(sys.argv)-1]
		get_positions(source_list, output_file)
