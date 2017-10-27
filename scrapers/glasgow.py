from bs4 import BeautifulSoup
import requests

import json
import re

uni_name = "University of Glasgow"
base_url = "http://www.gla.ac.uk"
text = []

urls = [
    "http://www.gla.ac.uk/coursecatalogue/courselist/?code=REG30200000&name=School+of+Computing+Science",
    "http://www.gla.ac.uk/coursecatalogue/courselist/?code=REG40100000&name=Adam+Smith+Business+School"
]

for url in urls:
    response = requests.get(url)

    links = []
    #print response.text
    uni_soup = BeautifulSoup(response.content, "html5lib")

    # The html response is messed up, there's a random /ul that stuffs up the parse r
    # have to rely on hardcoding

    div = uni_soup.find("form", attrs={"id":"printForm"})
    # print div

    # accordion_contents = div.find_all("div", attrs={"role":"tabpanel"})
    ul_elements = div.find_all("ul")
    for ul in ul_elements:
        a_elements = ul.find_all("a")
        for a in a_elements:
            links.append(a.get("href"))

    # for content in accordion_contents:

    print links
    for link in links:
        print "Pulling " + base_url + link
        response = requests.get(base_url + link)

        page_soup = BeautifulSoup(response.content, "html.parser")
        content = page_soup.find("div", class_="maincontent fullwidth")

        info = content.find("h1")
        m = re.search("(.*)\s([a-zA-Z]{3,8}\d{3,8})", info.text)
        course_code = m.group(2)
        course_title = m.group(1)

        link_obj = {
            "university": uni_name,
            "url": base_url + link,
            "course_code": course_code,
            "course_title": course_title,
            "text": str(content)
        }
        text.append(link_obj)

with open("glasgow.json", "w") as outfile:
  json.dump(text, outfile)
