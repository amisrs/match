from bs4 import BeautifulSoup
import requests

import json

urls = ["http://www.mcgill.ca/study/2017-2018/courses/search?f%5B0%5D=level%3Aundergraduate&f%5B1%5D=field_dept_code%3A0155",
"http://www.mcgill.ca/study/2017-2018/courses/search?f%5B0%5D=level%3Aundergraduate&f%5B1%5D=field_dept_code%3A0028",
"http://www.mcgill.ca/study/2017-2018/courses/search?f%5B0%5D=level%3Aundergraduate&f%5B1%5D=field_dept_code%3A0156"
]
base_url = "http://www.mcgill.ca"

# Get links
links = []

# Store links
for url in urls:
	next_page_url = url[len(base_url):]
	while True:
		response = requests.get(base_url + next_page_url)
		uni_soup = BeautifulSoup(response.content, "html.parser")
		# Append current page course links
		view = uni_soup.find("div", class_="view-content")
		courses_div = view.find_all("div")
		for course in courses_div:
			links_course = course.find("a")
			links.append(links_course.get("href"))
		# Go to next page
		next_button = uni_soup.find("li", class_="pager-next")
		if next_button == None:
			break;
		next_link = next_button.find("a")
		next_page_url = next_link.get("href")

with open("mcgillLinks.json", "w") as outfile:
	json.dump(links, outfile)

for link in links:
	# Go to stored url
	response = requests.get(base_url + link)
	# Store entire html markup
	uni_soup = BeautifulSoup(response.content, "html.parser")
	title = uni_soup.find("h1", id="page-title")
	content = uni_soup.find("div", class_="content")
	with open("mcgillText.json", "a") as outfile:
		json.dump("{" + str(title) + str(content) + "}\n", outfile)