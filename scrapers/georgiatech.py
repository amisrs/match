from bs4 import BeautifulSoup
import requests

import json

all_courses = []

with open("georgiatech.html", "r", encoding="utf8") as infile:
	file = infile.read()
	# Store entire html markup
	uni_soup = BeautifulSoup(file, "html.parser")
	courses = uni_soup.find_all("div")
	for course in courses:
		div_contents = course.find_all("span")
		if not len(div_contents) == 2:
			continue
		title = div_contents[0].getText().strip()
		is_valid_title = False
		count = 0
		for character in title:
			if count == 4:
				is_valid_title = True
			if character.isdigit():
				count += 1
		if not is_valid_title:
			continue

		to_insert = {}
		to_insert["university"] = "georgiatech"
		to_insert["course"] = title
		to_insert["text"] = div_contents[1].getText().strip()
		to_insert["url"] = "https://www.scheller.gatech.edu/degree-programs/undergraduate/files/BSBACourses.pdf"
		all_courses.append(to_insert)

	with open("georgiatechTextFormatted.json", "w") as outfile:
		json.dump(all_courses, outfile)