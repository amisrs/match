from bs4 import BeautifulSoup
import json

files = ["swanseaText.json"]
base_urls = ["https://intranet.swan.ac.uk/catalogue/"]
links = ["swanseaLinks.json"]
base_iterator = 0

course_links = []
with open(links[0], "r") as infile:
	course_links = eval(infile.read())
link_iterator = 0

for file in files:
	split_contents = []
	with open(file, "r") as infile:
		data = infile.read()
		start = 0
		end = 0
		reading = False
		for i in range (0, len(data)):
			if data[i] == "\"" and (i == 0 or data[i-1] != "\\"):
				if reading == False:
					start = i
					reading = True
				else:
					end = i
					#print("start " + str(start))
					#print("end " + str(end))
					text = data[start+1:end]
					text = text.replace("\\n", "")
					text = text.replace("\\", "")
					soup = BeautifulSoup(text, "html.parser")
					to_insert = {}
					to_insert["university"] = file[:-9]
					to_insert["course"] = soup.find("h2").getText().strip()
					to_insert["text"] = text
					to_insert["url"] = base_urls[base_iterator] + course_links[link_iterator]
					split_contents.append(to_insert)
					link_iterator = link_iterator + 1
					reading = False
	transformed_file = file[:-5] + "Formatted.json"
	with open(transformed_file, "w") as outfile:
		json.dump(split_contents, outfile)

	base_iterator = base_iterator + 1
