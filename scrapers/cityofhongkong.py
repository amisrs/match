from bs4 import BeautifulSoup
import requests

import json
import re

urls = ["http://www.cityu.edu.hk/ug/current/catalogue/B/B_course_AC.htm",
"http://www.cityu.edu.hk/ug/current/catalogue/B/B_course_EF.htm",
"http://www.cityu.edu.hk/ug/current/catalogue/B/B_course_IS.htm",
"http://www.cityu.edu.hk/ug/current/catalogue/B/B_course_MGT.htm",
"http://www.cityu.edu.hk/ug/current/catalogue/B/B_course_MS.htm",
"http://www.cityu.edu.hk/ug/current/catalogue/B/B_course_MS.htm",
"http://www.cityu.edu.hk/ug/current/catalogue/B/B_course_CS.htm"]
base_url = "http://www.cityu.edu.hk/ug/current/course/"

# Get links
links = []

# Store links
for url in urls:
	response = requests.get(url)
	uni_soup = BeautifulSoup(response.content, "html.parser")
	#print(uni_soup.prettify())
	div = uni_soup.find("body")
	links_element = div.find_all("a")
	for element in links_element:
		links.append(element.get("href")[10:])

with open("cityofhongkongLinks.json", "w") as outfile:
	json.dump(links, outfile)

for link in links:
	# Go to stored url
	response = requests.get(base_url + link)
	# Store entire html markup
	uni_soup = BeautifulSoup(response.content, "html.parser")
	div = uni_soup.find("div", class_="cityu-content-page")
	with open("cityofhongkongText.json", "a") as outfile:
		json.dump(str(div), outfile)