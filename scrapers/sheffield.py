from bs4 import BeautifulSoup
import requests

import json
import re

urls = ["http://www-online.shef.ac.uk:3001/pls/live/web_cal.cal3_unit_form?dept_code=INF&dept_name=Information+School&disp_year=17",
"http://www-online.shef.ac.uk:3001/pls/live/web_cal.cal3_unit_form?dept_code=COM&dept_name=Computer+Science&disp_year=17",
"http://www-online.shef.ac.uk:3001/pls/live/web_cal.cal3_unit_form?dept_code=ECN&dept_name=Economics&disp_year=17",
"http://www-online.shef.ac.uk:3001/pls/live/web_cal.cal3_unit_form?dept_code=MGT&dept_name=Management+School&disp_year=17"]
base_url = "http://www-online.shef.ac.uk:3001/pls/live/"

# Get links
links = []

# Store links
for url in urls:
	response = requests.get(url)
	uni_soup = BeautifulSoup(response.content, "html.parser")
	table1 = uni_soup.find("table", summary="Layout Table")
	table2 = table1.find("table")
	links_elements = table2.find_all("a")
	for element in links_elements:
		links.append(base_url + element.get("href"))

with open("sheffieldLinks.json", "w") as outfile:
	json.dump(links, outfile)

for link in links:
	# Go to stored url
	response = requests.get(link)
	# Store entire html markup
	uni_soup = BeautifulSoup(response.content, "html.parser")
	title = uni_soup.find(id="pageTitle").getText()
	desc = uni_soup.find("p", align="JUSTIFY")
	meta = uni_soup.find("p", align="LEFT")
	with open("sheffieldText.json", "a") as outfile:
		json.dump(str(title) + "\n" + str(desc) + "\n" + str(meta) + "\n", outfile)