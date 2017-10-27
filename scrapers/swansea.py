from bs4 import BeautifulSoup
import requests

import json
import re

url = "https://intranet.swan.ac.uk/catalogue/default.asp?type=modbydept&dept=any&ayr=17/18&detailOnly=false"
base_url = "https://intranet.swan.ac.uk/catalogue/"
# Go to url
response = requests.get(url)

# Get links
links = []
text = []

# Store links
uni_soup = BeautifulSoup(response.content, "html.parser")

div = uni_soup.find_all("div", class_="Modules")
links_element = div[0].find_all("a")
for element in links_element:
	links.append(element.get("href"))

with open("swanseaLinks.json", "w") as outfile:
	json.dump(links, outfile)

for link in links:
	# Go to stored url
	response = requests.get(base_url + link)
	# Store entire html markup
	uni_soup = BeautifulSoup(response.content, "html.parser")
	div = uni_soup.find_all("div", class_="moduleDetail")
	#text.append(div[0])
	with open("swanseaText.json", "a") as outfile:
		json.dump(str(div[0]), outfile)