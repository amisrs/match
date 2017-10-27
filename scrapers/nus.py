from bs4 import BeautifulSoup
import requests

import json
import re

urls = ["http://www.comp.nus.edu.sg/programmes/ug/is/curr/"]
base_url = "https://inetapps.nus.edu.sg/bulletin/msearch_view_full.aspx?modeCode="

# Get links
links = []

# Store links
for url in urls:
	response = requests.get(url)
	uni_soup = BeautifulSoup(response.content, "html.parser")
	div = uni_soup.find("div", itemprop="articleBody")
	links_element = div.find_all("p")
	for element in links_element:
		to_insert_all = element.getText()
		to_insert_words = to_insert_all.split()
		for to_insert in to_insert_words:
			if to_insert[:2].isalpha() and to_insert[2:6].isdigit() and len(to_insert) <= 8:
				links.append(to_insert[:6])
links = list(set(links))

with open("nusLinks.json", "w") as outfile:
	json.dump(links, outfile)

for link in links:
	# Go to stored url
	response = requests.get(base_url + link)
	# Store entire html markup
	uni_soup = BeautifulSoup(response.content, "html.parser")
	div = uni_soup.find("table", id="viewtbl")
	while div == None:
		# get session hack
		temp = requests.get("https://inetapps.nus.edu.sg/bulletin/msearch.aspx?code=&title=&desp=&semester=&fac=")
		response = requests.get(base_url + link)
		uni_soup = BeautifulSoup(response.content, "html.parser")
		print(uni_soup.prettify())
		div = uni_soup.find("table", id="viewtbl")

	with open("nusText.json", "a") as outfile:
		json.dump(str(div), outfile)