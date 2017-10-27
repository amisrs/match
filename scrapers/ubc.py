from bs4 import BeautifulSoup
import requests

import json

url = "https://mybcom.sauder.ubc.ca/courses-money-and-enrolment/courses"
base_url = "https://mybcom.sauder.ubc.ca"
# Go to url
response = requests.get(url)

# Get links
links = []
text = []

# Store links
uni_soup = BeautifulSoup(response.content, "html.parser")
# While there is a next page
while True:
	# Append current page course links
	view = uni_soup.find_all("div", class_="view-content")
	courses_div = view[0].find_all("div")
	for course in courses_div:
		links_course = course.find_all("a")
		links.append(links_course[0].get("href"))
	# Go to next page
	next_button_container = uni_soup.find_all("li", class_="pager-next first last")
	next_links = next_button_container[0].find_all("a")
	if len(next_links) == 0:
		break
	url = next_links[0].get("href")
	response = requests.get(base_url + url)
	uni_soup = BeautifulSoup(response.content, "html.parser")

with open("ubcLinks.json", "w") as outfile:
	json.dump(links, outfile)

for link in links:
	# Go to stored url
	response = requests.get(base_url + link)
	# Store entire html markup
	uni_soup = BeautifulSoup(response.content, "html.parser")
	section = uni_soup.find_all("section", class_="col-sm-12")
	#with open("ubc.json", "a") as outfile:
	#	json.dump(section, outfile)
	#text.append(str(section[0]))

	with open("ubcText.json", "a") as outfile:
		json.dump(str(section[0]), outfile)
